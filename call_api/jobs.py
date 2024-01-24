import json
import requests

JWT = ""


def create_job1():
    data = {
        "title": "Junior Python Engineer",
        "seniority": "0-2 years",
        "mandatory_knowledge": [
            "data structures",
            "c",
            "git"
        ],
        "optional_knowledge": [
            "python",
            "mysql"
        ]
    }

    response = requests.post("http://localhost:3000/jobs", data=json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def create_job2():
    data = {
        "title": "Senior Devops Engineer",
        "seniority": "8-12 years",
        "mandatory_knowledge": [
            "networking",
            "kubernetes",
            "AWS",
            "Terraform"
        ],
        "optional_knowledge": [
            "Jenkins",
            "VMWare",
            "hybrid infrastructure environments"
        ]
    }

    response = requests.post("http://localhost:3000/jobs", data=json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def list_jobs():
    response = requests.get("http://localhost:3000/jobs")
    print("Response", response.status_code, response.text)


def generate_questions():
    data = {
        "number": 8
    }
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/generate-questions", data=json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def list_questions():
    response = requests.get("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/questions")
    print("Response", response.status_code, response.text)


def add_candidate1():
    data = {
        "name": "Alex",
    }
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/candidates", json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def add_candidate2():
    data = {
        "name": "Marius",
    }
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/candidates", json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def add_candidate3():
    data = {
        "name": "Ciprian",
    }
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/candidates", json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def add_answer1():
    data = {
        "candidate_id": "640b934327329388c1a22d08",
        "text": "In a stack, the last element to be added is the first to be removed. In a queue, the first element "
                "to be added is the first element to be removed."
    }
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/questions/640b881542a1fcc523a53aa3/answer", json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def add_answer2():
    data = {
        "candidate_id": "640b970c19e0326312c5ac1b",
        "text": "Both the stack and the queue are data structures used to structure data sequentially. The stack is "
                "actually a subset of queues, more specifically a LIFO queue (last in, first out), in which the last "
                "element to be added is the first to be removed. The other type of queue is FIFO (first in, "
                "first out), in which the first element to be added is the first to be removed. In both stacks and "
                "queues, it is impossible to retrieve an element from the middle"
    }
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/questions/640b881542a1fcc523a53aa3/answer", json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def add_answer3():
    data = {
        "candidate_id": "640b9a69f5808b06ce379800",
        "text": "A stack is, like, a thing in which, like, things go first and leave first. And the queue is, like, "
                "another thing in which stuff goes first and leaves last"
    }
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/questions/640b881542a1fcc523a53aa3/answer", json.dumps(data), headers={
        "Content-Type": "application/json"
    })
    print("Response", response.status_code, response.text)


def generate_ideal_answer():
    response = requests.post("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/questions/640b881542a1fcc523a53aa5/generate-ideal-answer")
    print("Response", response.status_code, response.text)


def list_candidates():
    response = requests.get("http://localhost:3000/jobs/640b5fa1d2e8ac8d1b9bda4e/candidates", headers={
        "Authorization": f"Bearer {JWT}"
    })
    print("Response", response.status_code, response.text)


# add_answer1()
# add_answer2()
# add_answer3()
list_candidates()
