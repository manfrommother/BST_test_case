from django.test import TestCase, Client
from django.urls import reverse
from .models import Robot
import json

class RobotAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/robots/api/'
        
    def test_create_robot_success(self):
        """Тест успешного создания робота"""
        data = {
            "model": "R2",
            "version": "D2",
            "created": "2023-01-01 00:00:00"
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Robot.objects.count(), 1)
        self.assertEqual(Robot.objects.first().model, 'R2')

    def test_create_robot_invalid_model(self):
        """Тест создания робота с неверной моделью"""
        data = {
            "model": "R2D",  # 3 символа вместо 2
            "version": "D2",
            "created": "2023-01-01 00:00:00"
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_robot_invalid_version(self):
        """Тест создания робота с неверной версией"""
        data = {
            "model": "R2",
            "version": "D",  # 1 символ вместо 2
            "created": "2023-01-01 00:00:00"
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_robot_invalid_date(self):
        """Тест создания робота с неверной датой"""
        data = {
            "model": "R2",
            "version": "D2",
            "created": "invalid-date"
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)