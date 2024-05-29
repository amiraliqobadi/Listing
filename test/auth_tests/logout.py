import unittest
from unittest.mock import patch, MagicMock
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from sqlalchemy.orm.session import Session
from routers import auth


class TestLogout(unittest.TestCase):
    @patch('auth.get_current_user')
    @patch('auth.User')
    def test_logout_success(self, mock_user, mock_get_current_user):
        # Arrange
        mock_request = MagicMock(Request)
        mock_db = MagicMock(Session)
        mock_current_user = {'id': 1}
        mock_get_current_user.return_value = mock_current_user
        mock_user_instance = MagicMock()
        mock_user.query.filter.return_value.first.return_value = mock_user_instance

        # Act
        response = auth.logout(mock_request, current_user=mock_current_user, db=mock_db)

        # Assert
        self.assertIsInstance(response, RedirectResponse)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/docs#/")
        mock_request.session.clear.assert_called_once()
        response.delete_cookie.assert_any_call("access_token")
        response.delete_cookie.assert_any_call("refresh_token")

    @patch('auth.get_current_user')
    @patch('auth.User')
    def test_logout_user_not_found(self, mock_user, mock_get_current_user):
        # Arrange
        mock_request = MagicMock(Request)
        mock_db = MagicMock(Session)
        mock_current_user = {'id': 1}
        mock_get_current_user.return_value = mock_current_user
        mock_user.query.filter.return_value.first.return_value = None

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            auth.logout(mock_request, current_user=mock_current_user, db=mock_db)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "User not found")



