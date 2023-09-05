import uvicorn, random, string, bcrypt, jwt, time, auth
from datetime import datetime, timezone as timezone_module, timedelta
from dateutil import tz
import os

from fastapi import Request, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from typing_extensions import Annotated
from bson.objectid import ObjectId
from config import jwt_secret, app, auth_app, db, base_url

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@auth_app.post("/change-password")
def change_password(password: Annotated[str, Form()], new_password: Annotated[str, Form()], confirm_password: Annotated[str, Form()], request: Request):
	user = request.state.user

	if bcrypt.checkpw(password.encode("UTF-8"), user["password"]) != True:
		return {
			"status": "error",
			"message": "Password is in-correct."
		}

	if new_password != confirm_password:
		return {
			"status": "error",
			"message": "Password does not match."
		}

	db["users"].find_one_and_update({
		"_id": ObjectId(user["_id"])
	}, {
		"$set": {
			"password": bcrypt.hashpw(new_password.encode("UTF-8"), bcrypt.gensalt())
		}
	})

	return {
		"status": "success",
		"message": "Password has been updated."
	}

@auth_app.post("/save-profile")
def save_profile(name: Annotated[str, Form()], profile_image: UploadFile, request: Request):
	# profile_image.filename
	# profile_image.content_type
	# profile_image.size
	# profile_image.file

	user = request.state.user
	file_location = ""

	if profile_image and profile_image.size > 0:

		if not os.path.exists("uploads"):
			os.path.makedirs("uploads")

		file_location = "uploads/" + str(int(time.mktime(datetime.now().timetuple()))) + "-" + profile_image.filename
		with open(file_location, "wb+") as file_object:
			file_object.write(profile_image.file.read())

		if (os.path.exists(user["profile_image"])):
			os.remove(user["profile_image"])

	db["users"].find_one_and_update({
		"_id": ObjectId(user["_id"])
	}, {
		"$set": {
			"name": name,
			"profile_image": file_location
		}
	})

	return {
		"status": "success",
		"message": "Profile has been updated.",
		"file_location": base_url + "/" + file_location
	}

@auth_app.post("/logout")
def logout(request: Request):

	user = request.state.user

	db["users"].find_one_and_update({
		"_id": user["_id"]
	}, {
		"$unset": {
			"access_token": 1
		}
	})

	return {
		"status": "success",
		"message": "User has been logged-out."
	}

@auth_app.post("/me")
def get_user(timezone: Annotated[str, Form()], request: Request):

	user = request.state.user

	return {
		"status": "success",
		"message": "User has been fetched.",
		"user": {
			"_id": user["_id"],
			"name": user["name"],
			"email": user["email"],
			"profile_image": base_url + "/" + user["profile_image"]
		}
	}

@app.post("/login")
def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):

	user = db["users"].find_one({
		"email": email
	})

	if user == None:
		return {
			"status": "error",
			"message": "Email does not exists."
		}

	if bcrypt.checkpw(password.encode("UTF-8"), user["password"]) != True:
		return {
			"status": "error",
			"message": "Password is in-correct."
		}

	access_token = jwt.encode({
		"user_id": str(user["_id"]),
		"time": datetime.now(timezone_module.utc).timetuple(),
		"exp": datetime.now(timezone_module.utc) + timedelta(hours=24)
	}, jwt_secret, algorithm = "HS256")

	db["users"].find_one_and_update({
		"_id": user["_id"]
	}, {
		"$set": {
			"access_token": access_token
		}
	})

	return {
		"status": "success",
		"message": "Login successfully.",
		"access_token": access_token,
		"user": {
			"_id": str(user["_id"]),
			"name": user["name"],
			"email": user["email"],
			"profile_image": base_url + "/" + user["profile_image"]
		}
	}

@app.post("/signup")
def signup(name: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()]):

	user = db["users"].find_one({
		"email": email
	})

	if user != None:
		return {
			"status": "error",
			"message": "Email already exists."
		}

	db["users"].insert_one({
		"name": name,
		"email": email,
		"password": bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()),
		"created_at": datetime.now(timezone_module.utc)
	})

	return {
		"status": "success",
		"message": "Account has been created. Please login now."
	}

def convert_utc_to_local(timezone, utc):
	# Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz(timezone)

	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	utc = utc.replace(tzinfo=from_zone)

	# Convert time zone
	utc = utc.astimezone(to_zone).strftime("%b %d, %Y %H:%M:%S")

	return utc

app.mount("/", auth_app)

if __name__ == "__main__":
	uvicorn.run(app, port=port, host=host)
