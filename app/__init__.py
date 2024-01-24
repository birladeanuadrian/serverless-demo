import json
import os
from datetime import datetime, timedelta

from flask import Flask, Response, make_response, redirect, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from google.auth.transport import requests
from google.oauth2 import id_token

from .exceptions import InvalidDataException, NotFoundException, RateLimitException
from .extensions.openai_adapter import OpenaiAdapter, get_openai_adapter
from .models.answer import Answer
from .models.candidate import Candidate
from .models.job import Job
from .models.user import IdentityProvider, UserProfile
from .services.job_service import JobService
from .services.question_service import QuestionService
from .services.user_service import UserService
from .validation import validate_input
from .validation.create_job_form import CreateJobForm

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "mySecret")
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
DOMAIN = os.getenv("DOMAIN")
APP_URI = os.getenv("APP_URI")


@app.route("/register", methods=["POST"])
def register():
    user_service = UserService()
    username = request.json["username"]
    password = request.json["password"]
    user_service.register(username, password)
    return Response("ok", status=201)


@app.route("/oauth/google", methods=["POST"])
def google_auth():
    user_service = UserService()
    try:
        google_jwt = request.form.get("credential")
    # pylint: disable=bare-except
    except:
        google_jwt = request.json["credential"]

    try:
        id_info = id_token.verify_oauth2_token(google_jwt, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError as err:
        print("Value error", err, flush=True)
        raise err

    user_profile = UserProfile(
        email=id_info["email"],
        name=id_info["name"],
        picture_url=id_info["picture"],
        first_name=id_info["given_name"],
        last_name=id_info["family_name"],
        idp=IdentityProvider.GOOGLE,
    )

    auth_user_profile = user_service.login_with_idp(user_profile)
    cookies_expires_at = int((datetime.utcnow() + timedelta(hours=3)).timestamp())
    access_token = create_access_token(
        identity=auth_user_profile.email, expires_delta=timedelta(hours=3)
    )

    response = make_response(redirect(f"{APP_URI}/"))
    response.set_cookie(
        key="USER_PROFILE",
        value=json.dumps(auth_user_profile.as_json()),
        max_age=timedelta(hours=3),
        secure=bool(DOMAIN),
        domain=DOMAIN,
        expires=cookies_expires_at,
        samesite="Lax" if DOMAIN else None,
    )
    response.set_cookie(
        key="IDP_CREDENTIAL",
        value=google_jwt,
        max_age=timedelta(hours=3),
        secure=bool(DOMAIN),
        domain=DOMAIN,
        expires=cookies_expires_at,
        httponly=True,
        samesite="Lax" if DOMAIN else None,
    )
    response.set_cookie(
        key="APP_CREDENTIAL",
        value=access_token,
        max_age=timedelta(hours=3),
        secure=bool(DOMAIN),
        domain=DOMAIN,
        expires=cookies_expires_at,
        samesite="Lax" if DOMAIN else None,
    )
    return response


def generate_google_login():
    pass


@app.route("/login", methods=["POST"])
def login():
    user_service = UserService()
    username = request.json["username"]
    password = request.json["password"]
    user_service.login(username, password)
    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=3))
    return Response(json.dumps({"access_token": access_token}), status=200)


@app.route("/hello", methods=["GET"])
def hello():
    return "world"


@app.route("/jobs", methods=["POST"])
@jwt_required()
@validate_input(CreateJobForm)
def create_job():
    job_service = JobService()
    job = Job.build(request.json)
    job.set_id(None)
    job_service.create_job(job)
    return Response(json.dumps(job.as_json()), 200, headers={"Content-Type": "application/json"})


@app.route("/jobs", methods=["GET"])
@jwt_required()
def list_jobs():
    job_service = JobService()
    jobs = job_service.list_jobs()
    return json.dumps([x.as_json() for x in jobs])


@app.route("/jobs/<job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id: str):
    job_service = JobService()
    job = job_service.get_job(job_id)
    return json.dumps(job.as_json())


@app.route("/jobs/<job_id>/generate-questions", methods=["POST"])
@jwt_required()
def generate_questions(job_id: str):
    number = request.json["number"]
    openai_adapter = get_openai_adapter()
    question_service = QuestionService(openai_adapter)
    questions = question_service.generate_automatic_questions(job_id, number)
    return json.dumps([x.as_json() for x in questions])


@app.route("/jobs/<job_id>/questions", methods=["GET"])
@jwt_required()
def list_questions(job_id: str):
    openai_adapter = get_openai_adapter()
    question_service = QuestionService(openai_adapter)
    questions = question_service.list_questions(job_id)
    return json.dumps([x.as_json() for x in questions])


@app.route("/jobs/<job_id>/questions/<question_id>/generate-ideal-answer", methods=["POST"])
@jwt_required()
def generate_ideal_answer(job_id: str, question_id: str):
    openai_adapter = get_openai_adapter()
    question_service = QuestionService(openai_adapter)
    question = question_service.generate_ideal_answer(job_id, question_id)
    return json.dumps(question.as_json(), default=str)


@app.route("/jobs/<job_id>/candidates", methods=["POST"])
@jwt_required()
def add_candidate(job_id: str):
    job_service = JobService()
    candidate = Candidate.build({**request.json, "job_id": job_id})
    job_service.add_candidate(job_id, candidate)
    return Response(json.dumps(candidate.as_json()), 201)


@app.route("/jobs/<job_id>/candidates", methods=["GET"])
@jwt_required()
def list_candidates(job_id: str):
    job_service = JobService()
    candidates = job_service.list_candidates(job_id)
    return json.dumps([x.as_json() for x in candidates], default=str)


@app.route("/jobs/<job_id>/questions/<question_id>/answer", methods=["POST"])
@jwt_required()
def add_answer(job_id: str, question_id: str):
    openai_adapter = get_openai_adapter()
    question_service = QuestionService(openai_adapter)
    answer = Answer.build({**request.json, "question_id": question_id, "job_id": job_id})
    question_service.add_answer(job_id, answer)
    return Response(json.dumps(answer.as_json()), 201)


@app.errorhandler(NotFoundException)
def handle_not_found_error(error: NotFoundException):
    return Response(
        json.dumps({"message": str(error)}), 404, headers={"Content-Type": "application/json"}
    )


@app.errorhandler(InvalidDataException)
def handle_invalid_data(error: InvalidDataException):
    error_message = {"message": str(error), "errors": {str(error): "This field is extra."}}
    if error.field:
        error_message["errors"] = {error.field: "This field is extra."}
    return Response(json.dumps(error_message), 400, headers={"Content-Type": "application/json"})


@app.errorhandler(RateLimitException)
def handle_rate_limit_exception(error: RateLimitException):
    return Response(json.dumps({"message": str(error)}), status=429)
