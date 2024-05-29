import unittest
from routers.auth import validate_password  # Replace 'your_module' with the actual module name



class TestValidatePassword(unittest.TestCase):
    def test_validate_password_no_lowercase(self):
        # Test case: Password without at least one lowercase letter
        password = "A1@#%^&*89"
        self.assertFalse(validate_password(password))

    def test_validate_password_lowercase(self):
        # Test case: Password with at least one lowercase letter
        password = "a1@#%^&*89"
        self.assertTrue(validate_password(password))

    def test_validate_password_empty_string(self):
        # Test case: Empty string
        password = ""
        self.assertFalse(validate_password(password))

    def test_validate_password_no_special_character(self):
        # Test case: Password without at least one special character
        password = "a123456789"
        self.assertFalse(validate_password(password))

    def test_validate_password_no_uppercase(self):
        # Test case: Password without at least one uppercase letter
        password = "a1@#%^&*8"
        self.assertFalse(validate_password(password))

    def test_validate_password_no_number(self):
        # Test case: Password without at least one number
        password = "a@#%^&*"
        self.assertFalse(validate_password(password))

    def test_validate_password_too_short(self):
        # Test case: Password with less than 8 characters
        password = "a1@"
        self.assertFalse(validate_password(password))

    def test_validate_password_too_long(self):
        # Test case: Password with more than 20 characters
        password = "a1@#%^&*89abcdefghijk"
        self.assertFalse(validate_password(password))

