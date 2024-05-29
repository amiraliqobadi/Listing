import unittest
from unittest.mock import patch, MagicMock
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.query import Query
from routers import listing


class TestReadAll(unittest.TestCase):
    @patch('listing.Listing')
    def test_read_all_success(self, mock_listing):
        # Arrange
        mock_request = MagicMock()
        mock_user = {'id': 1}
        mock_db = MagicMock()
        mock_listings = [MagicMock(), MagicMock()]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_listings

        # Act
        response = listing.read_all(mock_request, mock_user, mock_db)

        # Assert
        self.assertEqual(response, jsonable_encoder(mock_listings))
        mock_db.query.assert_called_with(mock_listing)
        mock_db.query.return_value.filter.assert_called_with(mock_user['id'] == mock_listing.ownerId)
        mock_db.query.return_value.filter.return_value.all.assert_called_once()

    def test_read_all_unauthenticated(self):
        # Arrange
        mock_request = MagicMock()
        mock_user = None
        mock_db = MagicMock()

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            listing.read_all(mock_request, mock_user, mock_db)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, 'Authentication Failed')



