from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core import mail
from .models import Robot
from customers.models import Customer
from orders.models import Order
import json
from datetime import timedelta

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


class RobotReportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/report/download/'
        
        # Создаем тестовые данные
        for i in range(3):
            Robot.objects.create(
                model='R2',
                version='D2',
                created=timezone.now() - timedelta(days=1)
            )
            Robot.objects.create(
                model='R2',
                version='A1',
                created=timezone.now() - timedelta(days=2)
            )
        
        Robot.objects.create(
            model='R2',
            version='D2',
            created=timezone.now() - timedelta(days=10)
        )

    def test_report_download(self):
        """Тест скачивания отчета"""
        response = self.client.get(self.url)
        print(f"URL: {self.url}")
        print(f"Status code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        self.assertTrue(response.has_header('Content-Disposition'))
        self.assertTrue('attachment; filename="robots_report_' in response['Content-Disposition'])

    def test_empty_report(self):
        """Тест отчета без данных"""
        Robot.objects.all().delete()
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


class RobotNotificationTests(TestCase):
    def setUp(self):
        # Создаем клиента
        self.customer = Customer.objects.create(
            email='customer@example.com'
        )
        
        # Создаем ожидающий заказ
        self.order = Order.objects.create(
            customer=self.customer,
            robot_serial='R2-D2',
            status=Order.PENDING
        )

    def test_customer_notification(self):
        """Тест отправки уведомления при появлении робота"""
        # Создаем робота, который соответствует заказу
        Robot.objects.create(
            model='R2',
            version='D2',
            created=timezone.now()
        )
        
        # Проверяем, что письмо отправлено
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        
        # Проверяем содержимое письма
        self.assertEqual(sent_mail.subject, 'Робот доступен к заказу')
        self.assertEqual(sent_mail.to, ['customer@example.com'])
        self.assertIn('R2', sent_mail.body)
        self.assertIn('D2', sent_mail.body)

    def test_no_notification_for_different_robot(self):
        """Тест отсутствия уведомления при создании другого робота"""
        # Создаем робота другой модели
        Robot.objects.create(
            model='X5',
            version='LT',
            created=timezone.now()
        )
        
        # Проверяем, что письмо не отправлено
        self.assertEqual(len(mail.outbox), 0)

    def test_no_notification_for_completed_order(self):
        """Тест отсутствия уведомления для завершенного заказа"""
        # Меняем статус заказа на завершенный
        self.order.status = Order.COMPLETED
        self.order.save()
        
        # Создаем соответствующего робота
        Robot.objects.create(
            model='R2',
            version='D2',
            created=timezone.now()
        )
        
        # Проверяем, что письмо не отправлено
        self.assertEqual(len(mail.outbox), 0)