import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.api import api

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()
        self.app.testing = True

    @patch("app.api.api.get_users")
    def test_get_users_success(self, mock_get_users):
        mock_get_users.return_value = [{"id": 1, "name": "Test"}]
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.get_json())

    @patch("app.api.api.get_users")
    def test_get_users_not_found(self, mock_get_users):
        mock_get_users.return_value = []
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.get_json())

    @patch("app.api.api.add_user")
    def test_register_success(self, mock_add_user):
        payload = {"name": "Test", "email": "test@test.com", "password": "pass"}
        response = self.app.post('/register', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully", response.get_data(as_text=True))

    def test_register_missing_fields(self):
        payload = {"name": "", "email": "", "password": ""}
        response = self.app.post('/register', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("All fields are required", response.get_data(as_text=True))

    @patch("app.api.api.add_user", side_effect=Exception("DB error"))
    def test_register_exception(self, mock_add_user):
        payload = {"name": "Test", "email": "test@test.com", "password": "pass"}
        response = self.app.post('/register', json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertIn("DB error", response.get_data(as_text=True))

    @patch("app.api.api.authenticate_user")
    def test_login_success(self, mock_auth):
        mock_auth.return_value = {"id": 1, "name": "Test"}
        payload = {"email": "test@test.com", "password": "pass"}
        response = self.app.post('/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.get_json())

    @patch("app.api.api.authenticate_user")
    def test_login_fail(self, mock_auth):
        mock_auth.return_value = None
        payload = {"email": "test@test.com", "password": "wrong"}
        response = self.app.post('/login', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid email or password", response.get_data(as_text=True))

    @patch("app.api.api.get_diseases")
    def test_get_diseases_success(self, mock_get_diseases):
        mock_get_diseases.return_value = [{"id": 1, "name": "Flu"}]
        response = self.app.get('/diseases')
        self.assertEqual(response.status_code, 200)
        self.assertIn("diseases", response.get_json())

    @patch("app.api.api.get_diseases")
    def test_get_diseases_not_found(self, mock_get_diseases):
        mock_get_diseases.return_value = []
        response = self.app.get('/diseases')
        self.assertEqual(response.status_code, 404)
        self.assertIn("No diseases found", response.get_data(as_text=True))

    @patch("app.api.api.update_diseases")
    @patch("pandas.read_json")
    def test_update_diseases_success(self, mock_read_json, mock_update_diseases):
        mock_read_json.return_value = MagicMock(isnull=MagicMock(return_value=MagicMock(values=MagicMock(any=lambda: False))))
        response = self.app.put('/update_diseases_route', json={"diseases": "[]"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Diseases updated successfully", response.get_data(as_text=True))

    def test_update_diseases_no_data(self):
        response = self.app.put('/update_diseases_route', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("No data provided", response.get_data(as_text=True))

    @patch("pandas.read_json")
    def test_update_diseases_null_values(self, mock_read_json):
        mock_read_json.return_value = MagicMock(isnull=MagicMock(return_value=MagicMock(values=MagicMock(any=lambda: True))))
        response = self.app.put('/update_diseases_route', json={"diseases": "[]"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Data contains null values", response.get_data(as_text=True))

    @patch("app.api.api.update_diseases", side_effect=Exception("Update error"))
    @patch("pandas.read_json")
    def test_update_diseases_exception(self, mock_read_json, mock_update_diseases):
        mock_read_json.return_value = MagicMock(isnull=MagicMock(return_value=MagicMock(values=MagicMock(any=lambda: False))))
        response = self.app.put('/update_diseases_route', json={"diseases": "[]"})
        self.assertEqual(response.status_code, 500)
        self.assertIn("Update error", response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
