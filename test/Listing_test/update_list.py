import unittest
from unittest.mock import patch, MagicMock
from fastapi.exceptions import HTTPException
from datetime import datetime
from routers.listing import ListingRequest
from routers import listing


class TestUpdateList(unittest.TestCase):
    @patch('listing.Listing')
    @patch('listing.User')
    def test_update_list_success(self, mock_user, mock_listing):
        # Arrange
        mock_request = MagicMock()
        mock_user = {'id': 1}
        mock_db = MagicMock()
        mock_list_request = ListingRequest(
            type='updated_type',
            availableNow=False,
            address='updated_address'
        )
        mock_list_id = 1
        mock_list_model = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_list_model

        # Act
        listing.update_list(mock_request, mock_user, mock_db, mock_list_request, list_id=mock_list_id)

        # Assert
        mock_db.query.assert_called_with(mock_listing)
        mock_db.query.return_value.filter.assert_called_with(mock_listing.id == mock_list_id, mock_user.id == mock_user['id'])
        mock_db.query.return_value.filter.return_value.first.assert_called_once()
        self.assertEqual(mock_list_model.type, 'updated_type')
        self.assertEqual(mock_list_model.availableNow, False)
        self.assertEqual(mock_list_model.address, 'updated_address')
        self.assertIsInstance(mock_list_model.UpdatedAt, datetime)
        mock_db.add.assert_called_with(mock_list_model)
        mock_db.commit.assert_called_once()

    @patch('listing.Listing')
    @patch('listing.User')
    def test_update_list_not_found(self, mock_user, mock_listing):
        # Arrange
        mock_request = MagicMock()
        mock_user = {'id': 1}
        mock_db = MagicMock()
        mock_list_request = ListingRequest(
            type='updated_type',
            availableNow=False,
            address='updated_address'
        )
        mock_list_id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            listing.update_list(mock_request, mock_user, mock_db, mock_list_request, list_id=mock_list_id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, 'List not found')



