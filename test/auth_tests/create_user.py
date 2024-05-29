import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from routers.auth import create_user
from models import User


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        self.create_user_request = MagicMock()
        self.create_user_request.userName = "testuser"
        self.create_user_request.fullName = "Test User"
        self.create_user_request.email = "test@example.com"
        self.create_user_request.hashedPassword = "Password123!"
        self.create_user_request.DoB = "1990-01-01"
        self.create_user_request.gender = "Male"

        self.db = MagicMock(spec=Session)

    @patch('Listing.routers.auth.validate_password')
    def test_create_user_with_valid_password(self, mock_validate_password):
        mock_validate_password.return_value = True

        create_user(request=None, create_user_request=self.create_user_request, db=self.db)

        self.db.add.assert_called_once_with(User(
            userName=self.create_user_request.userName,
            fullName=self.create_user_request.fullName,
            email=self.create_user_request.email,
            hashedPassword=mock_validate_password.return_value,
            DoB=self.create_user_request.DoB,
            gender=self.create_user_request.gender
        ))
        self.db.commit.assert_called_once()

    @patch('Listing.routers.auth.validate_password')
    def test_create_user_with_invalid_password(self, mock_validate_password):
        mock_validate_password.return_value = False

        with self.assertRaises(HTTPException) as context:
            create_user(request=None, create_user_request=self.create_user_request, db=self.db)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, "Enter valid Password. Password should contain at least 1 uppercase, 1 lowercase, 1 number, 1 special character and should be 8-20 characters long.")
        self.db.add.assert_not_called()
        self.db.commit.assert_not_called()


