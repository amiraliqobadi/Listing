import unittest
from unittest.mock import patch, MagicMock
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.requests import Request
from routers import auth


class TestLoginForAccessToken(unittest.TestCase):
    @patch('auth.authenticate_user')
    @patch('auth.create_access_token')
    @patch('auth.redis_conn')
    def test_login_for_access_token_success(self, mock_redis_conn, mock_create_access_token, mock_authenticate_user):
        # Arrange
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.userName = 'testuser'
        mock_authenticate_user.return_value = mock_user
        mock_create_access_token.return_value = 'test_access_token'
        mock_redis_conn.get.return_value = None
        form_data = OAuth2PasswordRequestForm(username='testuser', password='testpassword')

        # Act
        response = auth.login_for_access_token(Request(), form_data=form_data, db=MagicMock(Session))

        # Assert
        self.assertEqual(response, {'access_token': 'test_access_token', 'token_type': 'bearer'})
        mock_authenticate_user.assert_called_with('testuser', 'testpassword', MagicMock(Session))
        mock_create_access_token.assert_called_with(data={'sub': 'testuser', 'id': 1})
        mock_redis_conn.get.assert_called_with('user:1:session')
        mock_redis_conn.delete.assert_not_called()
        mock_redis_conn.set.assert_any_call('user:1:session', 'test_access_token')
        mock_redis_conn.set.assert_any_call('session:test_access_token', 1, ex=3600)

    @patch('auth.authenticate_user')
    def test_login_for_access_token_invalid_credentials(self, mock_authenticate_user):
        # Arrange
        mock_authenticate_user.return_value = None
        form_data = OAuth2PasswordRequestForm(username='testuser', password='testpassword')

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            auth.login_for_access_token(Request(), form_data=form_data, db=MagicMock(Session))

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, 'Incorrect username or password')
        self.assertEqual(context.exception.headers, {'WWW-Authenticate': 'Bearer'})


