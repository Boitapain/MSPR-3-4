import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.frontend.login import login

class TestLogin(unittest.TestCase):
    @patch("app.frontend.login.requests.post")
    @patch("streamlit.text_input")
    @patch("streamlit.button")
    @patch("streamlit.error")
    @patch("streamlit.session_state", new_callable=dict)
    def test_successful_login(self, mock_session_state, mock_error, mock_button, mock_text_input, mock_post):
        # Mock user input
        mock_text_input.side_effect = ["test@example.com", "password123"]
        mock_button.side_effect = [True, False]  # Simulate "Login" button click

        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"user": {"id": 1, "name": "Test User"}}

        # Call the login function
        login()

        # Assertions
        self.assertTrue(mock_session_state['logged_in'])
        self.assertEqual(mock_session_state['page'], 'dashboard')
        self.assertEqual(mock_session_state['user'], {"id": 1, "name": "Test User"})

    @patch("app.frontend.login.requests.post")
    @patch("streamlit.text_input")
    @patch("streamlit.button")
    @patch("streamlit.error")
    def test_failed_login(self, mock_error, mock_button, mock_text_input, mock_post):
        # Mock user input
        mock_text_input.side_effect = ["test@example.com", "wrongpassword"]
        mock_button.side_effect = [True, False]  # Simulate "Login" button click

        # Mock API response
        mock_post.return_value.status_code = 401

        # Call the login function
        login()

        # Assertions
        mock_error.assert_called_once_with("Invalid email or password")

if __name__ == "__main__":
    unittest.main()
