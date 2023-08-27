from fastapi import Request
import jwt, time
from bson.objectid import ObjectId
from datetime import datetime
from config import jwt_secret, auth_app, db

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@auth_app.middleware("http")
async def get_user(request: Request, call_next):
	user = None
	try:
		authorization = request.headers["Authorization"]
		access_token = authorization.split("Bearer ")[1]

		payload = jwt.decode(access_token, jwt_secret, algorithms = "HS256")
	
		dt1 = time.mktime(datetime.now().timetuple())
		dt2 = payload["exp"]
		delta = dt2 - dt1
		delta = delta / 60 / 60

		if delta <= 0:
			return JSONResponse(content=jsonable_encoder({
				"status": "error",
				"message": "You have been logged-out."
			}))

		user = db["users"].find_one({
			"$and": [{
				"_id": ObjectId(payload["user_id"])
			}, {
				"access_token": access_token
			}]
		})

		if user == None:
			return JSONResponse(content=jsonable_encoder({
				"status": "error",
				"message": "You have been logged-out."
			}))

		user["_id"] = str(user["_id"])
		request.state.user = user

		response = await call_next(request)
		return response

	except Exception as error:
		return JSONResponse(content=jsonable_encoder({
			"status": "error",
			"message": "You have been logged-out.",
			"error": str(error)
		}))