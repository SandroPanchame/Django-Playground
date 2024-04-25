from rest_framework.test import APIClient

class TestCreateCollection:
# test_ <-naming convention for pytest
    def test_if_user_is_anonymous_returns_401(self):
        # Arrange
        
        # Act
        return