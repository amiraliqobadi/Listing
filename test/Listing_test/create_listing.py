import unittest
from unittest.mock import patch, MagicMock
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from routers.listing import ListingRequest
from routers import listing


class TestCreateListing(unittest.TestCase):
    @patch('listing.Listing')
    def test_create_listing_success(self, mock_listing):
        # Arrange
        mock_request = MagicMock()
        mock_user = {'id': 1}
        mock_listing_request = ListingRequest(
            type='test_type',
            availableNow=True,
            address='test_address'
        )
        mock_db = MagicMock()
        mock_listing_instance = MagicMock()
        mock_listing.return_value = mock_listing_instance

        # Act
        response = listing.create_listing(mock_request, mock_user, mock_listing_request, mock_db)

        # Assert
        self.assertEqual(response, jsonable_encoder(mock_listing_instance))
        mock_listing.assert_called_with(
            type='test_type',
            availableNow=True,
            address='test_address',
            ownerId=mock_user['id']
        )
        mock_db.add.assert_called_with(mock_listing_instance)
        mock_db.commit.assert_called_once()

    def test_create_listing_unauthenticated(self):
        # Arrange
        mock_request = MagicMock()
        mock_user = None
        mock_listing_request = ListingRequest(
            type='test_type',
            availableNow=True,
            address='test_address'
        )
        mock_db = MagicMock()

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            listing.create_listing(mock_request, mock_user, mock_listing_request, mock_db)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, 'Authentication Failed')


