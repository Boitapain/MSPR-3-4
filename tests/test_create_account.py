import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.frontend.create_account import create_account

class TestCreateAccount(unittest.TestCase):
    @patch("app.frontend.create_account.requests.post")
    @patch("streamlit.text_input")
    @patch("streamlit.button")
    @patch("streamlit.error")
    @patch("streamlit.success")
    def test_empty_fields(self, mock_success, mock_error, mock_button, mock_text_input, mock_post):
        # Mock Streamlit inputs
        mock_text_input.side_effect = ["", "", "", ""]  # All fields empty
        mock_button.side_effect = [False, True]  # Register button clicked

        # Call the function
        create_account()

        # Assert error message for empty fields
        mock_error.assert_called_once_with("All fields are required")
        mock_success.assert_not_called()

    @patch("app.frontend.create_account.requests.post")
    @patch("streamlit.text_input")
    @patch("streamlit.button")
    @patch("streamlit.error")
    @patch("streamlit.success")
    def test_passwords_do_not_match(self, mock_success, mock_error, mock_button, mock_text_input, mock_post):
        # Mock Streamlit inputs
        mock_text_input.side_effect = ["John Doe", "john@example.com", "password123", "password456"]
        mock_button.side_effect = [False, True]  # Register button clicked

        # Call the function
        create_account()

        # Assert error message for password mismatch
        mock_error.assert_called_once_with("Passwords do not match")
        mock_success.assert_not_called()

    @patch("app.frontend.create_account.requests.post")
    @patch("streamlit.text_input")
    @patch("streamlit.button")
    @patch("streamlit.error")
    @patch("streamlit.success")
    def test_successful_registration(self, mock_success, mock_error, mock_button, mock_text_input, mock_post):
        # Mock Streamlit inputs
        mock_text_input.side_effect = ["John Doe", "john@example.com", "password123", "password123"]
        mock_button.side_effect = [False, True]  # Register button clicked

        # Mock successful response from requests.post
        mock_post.return_value = MagicMock(status_code=201)

        # Call the function
        create_account()

        # Assert success message
        mock_success.assert_called_once_with("Account created successfully!")
        mock_error.assert_not_called()

    @patch("app.frontend.create_account.requests.post")
    @patch("streamlit.text_input")
    @patch("streamlit.button")
    @patch("streamlit.error")
    @patch("streamlit.success")
    def test_failed_registration(self, mock_success, mock_error, mock_button, mock_text_input, mock_post):
        # Mock Streamlit inputs
        mock_text_input.side_effect = ["John Doe", "john@example.com", "password123", "password123"]
        mock_button.side_effect = [False, True]  # Register button clicked

        # Mock failed response from requests.post
        mock_post.return_value = MagicMock(status_code=400, json=lambda: {"message": "Email already exists"})

        # Call the function
        create_account()

        # Assert error message for failed registration
        mock_error.assert_called_once_with("Failed to create account: Email already exists")
        mock_success.assert_not_called()

if __name__ == "__main__":
    unittest.main()
