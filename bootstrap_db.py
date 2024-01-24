from dotenv import load_dotenv
load_dotenv()

import os
import pymongo
from pymongo.collection import Collection


conn_url = os.getenv("MONGO_URI")
conn = pymongo.MongoClient(conn_url)
db = conn.get_database("technical-screen")

users_coll: Collection = db["users"]
users_coll.create_index("username", unique=True)
users_coll.create_index([("idp", pymongo.ASCENDING), ("email", pymongo.ASCENDING)], unique=True)

questions_coll: Collection = db["questions"]
questions_coll.create_index([("job_id", pymongo.ASCENDING), ("index", pymongo.ASCENDING)])

answers_coll = db["answers"]
answers_coll.create_index([("job_id", pymongo.ASCENDING), ("question_id", pymongo.ASCENDING), ("candidate_id", pymongo.ASCENDING)], unique=True)

extracted_answers_coll = db["extracted_answers"]
extracted_answers_coll.create_index([("job_id", pymongo.ASCENDING), ("candidate_id", pymongo.ASCENDING)], unique=True)
