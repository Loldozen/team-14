from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

User = get_user_model()

class UserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='name1',
            last_name='name2',
            password='randompassword'
        )
        self.create_url = reverse('signup')

    def test_create_user(self):

        data = {
            'email':'random@gmail.com',
            'first_name':'test1',
            'last_name':'test2',
            'password':'anypassword'
        }
        response = self.client.post(self.create_url,data,format='json')

        self.assertEqual(User.objects.count(),2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertFalse('password' in response.data)
    
    def test_create_user_with_short_password(self):

        data = {
            'email':'random@gmail.com',
            'first_name':'test1',
            'last_name':'test2',
            'password':'any'
        }
        response = self.client.post(self.create_url, data, format=None) 
        # Should be True uf the user creation is not successful
        # because the pasword is short
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check the number of user account created, 
        # should be 1 (the user from the initial setUp function)
        self.assertEqual(User.objects.count(), 1)
        # check that the password field should not be populated
        #  because the minimum is 8 characters
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):

        data = {
            'email':'random@gmail.com',
            'first_name':'test1',
            'last_name':'test2',
            'password':''
        }
        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)
    
    def test_create_user_with_no_email(self):
        
        data = {
            'email':'',
            'first_name':'test1',
            'last_name':'test2',
            'password':'anypassword'
        }
        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_existing_email(self):

        data = {
            'email':'test@example.com',
            'first_name':'test1',
            'last_name':'test2',
            'password':'anypassword'
        }
        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)