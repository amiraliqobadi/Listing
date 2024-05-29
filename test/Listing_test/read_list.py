import unittest
from unittest.mock import patch, MagicMock
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from routers import listing


class TestReadList(unittest.TestCase):
    @patch('listing.Listing')
    def test_read_list_success(self, mock_listing):
        # Arrange
        mock_request = MagicMock()
        mock_db = MagicMock()
        mock_list_id = 1
        mock_list_model = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_list_model

        # Act
        response = listing.read_list(mock_request, mock_db, list_id=mock_list_id)

        # Assert
        self.assertEqual(response, jsonable_encoder(mock_list_model))
        mock_db.query.assert_called_with(mock_listing)
        mock_db.query.return_value.filter.assert_called_with(mock_listing.id == mock_list_id)
        mock_db.query.return_value.filter.return_value.first.assert_called_once()

    @patch('listing.Listing')
    def test_read_list_not_found(self, mock_listing):
        # Arrange
        mock_request = MagicMock()
        mock_db = MagicMock()
        mock_list_id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            listing.read_list(mock_request, mock_db, list_id=mock_list_id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, 'Not found any Listing')

