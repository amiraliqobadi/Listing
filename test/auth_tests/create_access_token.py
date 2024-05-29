import unittest
from unittest.mock import patch
from typing import Dict
import jwt
from routers.auth import create_access_token, SECRET_KEY, ALGORITHM


class TestCreateAccessToken(unittest.TestCase):
    @patch('auth.jwt.encode')
    def test_create_access_token(self, mock_jwt_encode):
        # Arrange
        mock_data: Dict[str, str] = {
            'sub': 'test_user',
            'scope': 'test_scope'
        }
        mock_encoded_jwt = 'encoded_jwt'
        mock_jwt_encode.return_value = mock_encoded_jwt

        # Act
        result = create_access_token(mock_data)

        # Assert
        mock_jwt_encode.assert_called_with(mock_data.copy(), SECRET_KEY, algorithm=ALGORITHM)
        self.assertEqual(result, mock_encoded_jwt)



