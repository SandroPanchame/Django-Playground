from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


# pytest-watch is for continous testing

# Ran into an issue involving pytest, installed pytest-django.(fixed)
# pytest-django introduces additional decorators.
 
@pytest.mark.django_db
class TestCreateCollection:
# test_ <-naming convention for pytest
    # @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Arrange
        # Act
        # client = APIClient()
        # response = client.post('/store/collections/', {'title': 'a'})
        response = create_collection({'title': 'a'})
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self,authenticate, create_collection):
        # client = APIClient()
        # api_client.force_authenticate(user={})
        # response = api_client.post('/store/collections/', {'title': 'a'})
        authenticate(is_staff=False)
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        # client = APIClient()
        # # don't need to query the database, just create the user object
        # client.force_authenticate(user=User(is_staff=True))
        # response = client.post('/store/collections/', {'title': ''})
        # best practice: tests should have 1 responsibility
        # this test has two assertions because they are related 
        
        authenticate(is_staff=True)
        response = create_collection({'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
           
    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):
        # client = APIClient()

        # client.force_authenticate(user=User(is_staff=True))
        # response = client.post('/store/collections/', {'title': 'a'})
        authenticate(is_staff=True)
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0