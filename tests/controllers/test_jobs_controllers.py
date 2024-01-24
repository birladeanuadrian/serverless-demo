import json
import unittest
from datetime import timedelta
from unittest.mock import MagicMock

from app import app, create_access_token


class JobsControllerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            self.token = create_access_token(
                "test@project-osiris.net", expires_delta=timedelta(hours=1)
            )

    def test_create_job_with_valid_parameters(self):
        with unittest.mock.patch("app.JobService", return_value=MagicMock()):
            response = self.app.post(
                "/jobs",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "title": "Junior Engineer",
                        "seniority": "0-5",
                        "mandatory_knowledge": ["python", "mysql"],
                        "optional_knowledge": "kubernetes",
                    }
                ),
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json,
                {
                    "mandatory_knowledge": ["python", "mysql"],
                    "optional_knowledge": "kubernetes",
                    "seniority": "0-5",
                    "title": "Junior Engineer",
                },
            )

    def test_create_job_without_title(self):
        with unittest.mock.patch("app.JobService", return_value=MagicMock()):
            response = self.app.post(
                "/jobs",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "seniority": "0-5",
                        "mandatory_knowledge": ["python", "mysql"],
                        "optional_knowledge": "kubernetes",
                    }
                ),
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json,
                {"errors": {"title": ["This field is required."]}, "message": "Invalid input"},
            )

    def test_create_job_with_empty_title(self):
        with unittest.mock.patch("app.JobService", return_value=MagicMock()):
            response = self.app.post(
                "/jobs",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "title": "",
                        "seniority": "0-5",
                        "mandatory_knowledge": ["python", "mysql"],
                        "optional_knowledge": "kubernetes",
                    }
                ),
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json,
                {"errors": {"title": ["This field is required."]}, "message": "Invalid input"},
            )

    def test_create_job_without_seniority(self):
        with unittest.mock.patch("app.JobService", return_value=MagicMock()):
            response = self.app.post(
                "/jobs",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "title": "Senior Python developer",
                        "mandatory_knowledge": ["python", "mysql"],
                        "optional_knowledge": "kubernetes",
                    }
                ),
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json,
                {"errors": {"seniority": ["This field is required."]}, "message": "Invalid input"},
            )

    def test_create_job_with_additional_fields(self):
        with unittest.mock.patch("app.JobService", return_value=MagicMock()):
            response = self.app.post(
                "/jobs",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "title": "Senior Python developer",
                        "seniority": "0-2",
                        "random": "stuff",
                        "mandatory_knowledge": ["python", "mysql"],
                        "optional_knowledge": "kubernetes",
                    }
                ),
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json,
                {
                    "errors": {"random": "This field is extra."},
                    "message": "Invalid field identified.",
                },
            )


if __name__ == "__main__":
    unittest.main()
