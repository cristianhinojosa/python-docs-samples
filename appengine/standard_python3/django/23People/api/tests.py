import json

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


class ApiTest(TestCase):
    token =""
    def set_up(self):
        User = get_user_model()
        email = 'user@test.com'
        password = 'userpass1'
        username = 'user'
        user = User.objects.create_user(username=username, email=email, password=password)
        obtain_url = reverse('token_obtain_pair')
        response = self.client.post(obtain_url, {'username': username, 'password': password}, format='json')
        user.is_active = True
        user.save()
        self.token = response.data['access']
        return self.token

    def test_invalid_rut(self):
        self.token = ApiTest.set_up(self)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.token)
        # create drug:
        drug =  {"name": "cristiano","code": 1111,"description": "dsfdsfdsf"}
        drug_response  = client.post('/drug/', json.dumps(drug),   content_type='application/json')
        # create vaccination with bad Rut:
        vaccination = {"rut": "16.074.228-2", "dose": "0.20","date": "2020-08-13","drug": 1}
        vaccination_response  = client.post('/vaccination/', json.dumps(vaccination),   content_type='application/json')
        print("\nThe Invalid Rut Status is = %s" % (vaccination_response.status_code))        
        self.assertEqual(vaccination_response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_valid_rut(self):
        self.token = ApiTest.set_up(self)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.token)
        # create drug:
        drug =  {"name": "dsds","code": 2222,"description": "dsfdsfdsf"}
        drug_response  = client.post('/drug/', json.dumps(drug),   content_type='application/json')
        # create vaccination with bad Rut:
        vaccination = {"rut": "16.074.228-3", "dose": "0.20","date": "2020-08-13","drug": 2}
        vaccination_response  = client.post('/vaccination/', json.dumps(vaccination),   content_type='application/json')
        print("\nThe Valid Rut Status is = %s" % (vaccination_response.status_code))       
        self.assertEqual(vaccination_response.status_code, status.HTTP_201_CREATED)
        

