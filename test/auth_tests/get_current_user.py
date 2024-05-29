import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from routers.auth import get_current_user, User, oath2_bearer


class TestGetCurrentUser(unittest.TestCase):
    @patch('auth.jwt.decode')
    @patch('auth.get_db')
    def test_valid_token(self, mock_get_db, mock_jwt_decode):
        # Arrange
        mock_token = 'valid_token'
        mock_user_id = 'test_user'
        mock_user = User(id=1, userName=mock_user_id)
        mock_db = MagicMock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_get_db.return_value = mock_db

        # Act
        result = get_current_user(mock_token, mock_db)

        # Assert

        mock_jwt_decode.assert_called_with(mock_token, 'SECRET_KEY', algorithms=['ALGORITHM'])
        mock_db.query.assert_called_with(User)
        mock_db.query.return_value.filter.assert_called_with(User.userName == mock_user_id)

    @patch('auth.jwt.decode')
    @patch('auth.get_db')
    def test_invalid_token(self, mock_get_db, mock_jwt_decode):
        # Arrange
        mock_token = 'invalid_token'
        mock_jwt_decode.side_effect = Exception('Invalid token')
        mock_db = MagicMock(spec=Session)

        # Act and Assert
        with self.assertRaises(HTTPException):
            get_current_user(mock_token, mock_db)

        mock_jwt_decode.assert_called_with(mock_token, 'SECRET_KEY', algorithms=['ALGORITHM'])

    @patch('auth.get_db')
    def test_user_not_found(self, mock_get_db):
        # Arrange
        mock_token = 'valid_token'
        mock_user_id = 'test_user'
        mock_db = MagicMock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        mock_get_db.return_value = mock_db

        # Act and Assert
        with self.assertRaises(HTTPException):
            get_current_user(mock_token, mock_db)

        mock_db.query.assert_called_with(User)
        mock_db.query.return_value.filter.assert_called_with(User.userName == mock_user_id)



