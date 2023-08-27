import uvicorn, random, string, bcrypt, jwt, time, auth
from datetime import datetime, timezone as timezone_module, timedelta
from dateutil import tz
from fastapi import Request, Form
from typing_extensions import Annotated
from fastapi.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId
from config import jwt_secret, app, auth_app, db

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/logout")
def logout(access_token: Annotated[str, Form()]):
	try:
		payload = jwt.decode(access_token, jwt_secret, algorithms = "HS256")

		db["users"].find_one_and_update({
			"_id": ObjectId(payload["user_id"])
		}, {
			"$unset": {
				"access_token": 1
			}
		})

		return {
			"status": "success",
			"message": "User has been logged-out."
		}
	except Exception as error:
		return {
			"status": "error",
			"message": "You have been logged-out.",
			"error": str(error)
		}

@auth_app.post("/me")
def get_user(timezone: Annotated[str, Form()], access_token: Annotated[str, Form()], request: Request):

	user = request.state.user

	return {
		"status": "success",
		"message": "User has been fetched.",
		"user": {
			"_id": user["_id"],
			"name": user["name"],
			"email": user["email"]
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
			"email": user["email"]
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
	uvicorn.run(app, port=8000, host="127.0.0.1")
