from django.test.client import RequestFactory
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework import status

from api.logic.integrator_factory import IntegratorFactory
from .mock_classes import AutenticationFailedSourceMock, AutenticationNoneSourceMock
from .mock_classes import FetchFailedSourceMock, FetchNoneSourceMock
from .mock_classes import ParseFailedSourceMock, ParseNoneSourceMock, ParseValidResponseSourceMock

class TestsIntegratorFactory(APITestCase):
    rf = RequestFactory()
    valid_request = {
      'username': 'John',
      'password': 'Snow',
      'start_date': '2024-12-01',
      'end_date': '2024-12-11'
    }
    invalid_request = {}

    def test_invalid_request(self):
      integrator = IntegratorFactory(AutenticationFailedSourceMock)     

      request = self.rf.post('/', self.invalid_request)
      response = integrator(request)
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_autentication(self):
        integrator = IntegratorFactory(AutenticationFailedSourceMock)     

        request = self.rf.post('/', self.valid_request)
        response = integrator(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_autentication_none(self):
        integrator = IntegratorFactory(AutenticationNoneSourceMock)     

        request = self.rf.post('/', self.valid_request)
        response = integrator(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_failed_fetch(self):
        integrator = IntegratorFactory(FetchFailedSourceMock)     

        request = self.rf.post('/', self.valid_request)
        response = integrator(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_none(self):
        integrator = IntegratorFactory(FetchNoneSourceMock)     

        request = self.rf.post('/', self.valid_request)
        response = integrator(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_failed_parse(self):
        integrator = IntegratorFactory(ParseFailedSourceMock)     

        request = self.rf.post('/', self.valid_request)
        response = integrator(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_parse_none(self):
        integrator = IntegratorFactory(ParseNoneSourceMock)     

        request = self.rf.post('/', self.valid_request)
        response = integrator(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_happy_path(self):
        integrator = IntegratorFactory(ParseValidResponseSourceMock)

        request = self.rf.post('/', self.valid_request)
        response = integrator(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)