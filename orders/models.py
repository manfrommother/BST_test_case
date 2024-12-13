from django.db import models
from django.conf import settings
from customers.models import Customer


from django.db import models
from django.utils import timezone
from customers.models import Customer

class Order(models.Model):
    """Модель заказа с добавлением статуса"""
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'В ожидании'),
        (COMPLETED, 'Завершен'),
        (CANCELLED, 'Отменен'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    @property
    def robot_model(self):
        """Получаем модель робота из серийного номера"""
        return self.robot_serial[:2]
        
    @property
    def robot_version(self):
        """Получаем версию робота из серийного номера"""
        return self.robot_serial[3:]
