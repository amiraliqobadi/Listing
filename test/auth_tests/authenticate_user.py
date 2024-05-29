import unittest
from unittest import result
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from routers.auth import authenticate_user, User, bcrypt_context


class TestAuthenticateUser(unittest.TestCase):
    @patch('auth.bcrypt_context.verify')
    @patch('auth.User')
    def test_valid_credentials(self, mock_user, mock_bcrypt_verify):

        mock_username = 'testuser'
        mock_password = 'testpassword'
        mock_user_obj = MagicMock(spec=User)
        mock_user_obj.hashedPassword = 'hashed_password'
        mock_db = MagicMock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user_obj
        mock_bcrypt_verify.return_value = True

        mock_db.query.assert_called_with(User)
        mock_db.query.return_value.filter.assert_called_with(User.userName == mock_username)
        mock_bcrypt_verify.assert_called_with(mock_password, mock_user_obj.hashedPassword)
        self.assertEqual(result, mock_user_obj)

    @patch('auth.bcrypt_context.verify')
    @patch('auth.User')
    def test_invalid_username(self, mock_user, mock_bcrypt_verify):

        mock_username = 'invaliduser'
        mock_password = 'testpassword'
        mock_db = MagicMock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None


        result = authenticate_user(mock_username, mock_password, mock_db)


        mock_db.query.assert_called_with(User)
        mock_db.query.return_value.filter.assert_called_with(User.userName == mock_username)
        self.assertFalse(result)

    @patch('auth.bcrypt_context.verify')
    @patch('auth.User')
    def test_invalid_password(self, mock_user, mock_bcrypt_verify):

        mock_username = 'testuser'
        mock_password = 'invalidpassword'
        mock_user_obj = MagicMock(spec=User)
        mock_user_obj.hashedPassword = 'hashed_password'
        mock_db = MagicMock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user_obj
        mock_bcrypt_verify.return_value = False


        mock_db.query.assert_called_with(User)
        mock_db.query.return_value.filter.assert_called_with(User.userName == mock_username)
        mock_bcrypt_verify.assert_called_with(mock_password, mock_user_obj.hashedPassword)
        self.assertFalse(result)



