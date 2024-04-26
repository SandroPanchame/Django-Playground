from rest_framework.test import APIClient
from rest_framework import status
import pytest

# Ran into an issue involving pytest, installed pytest-django.(fixed)
# pytest-django introduces additional decorators.
 
@pytest.mark.django_db
class TestCreateCollection:
# test_ <-naming convention for pytest
    def test_if_user_is_anonymous_returns_401(self):
        # Arrange
        
        # Act
        client = APIClient()
        response = client.post('/store/collections/', {'title': 'a'})
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED