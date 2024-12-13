from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Robot
from orders.models import Order

@receiver(post_save, sender=Robot)
def notify_customers_about_robot(sender, instance, created, **kwargs):
    """Отправляем уведомления клиентам при создании нового робота"""
    if not created:
        return
        
    # Формируем серийный номер робота
    robot_serial = f"{instance.model}-{instance.version}"
    
    # Ищем ожидающие заказы на этого робота
    pending_orders = Order.objects.filter(
        robot_serial=robot_serial,
        status=Order.PENDING
    ).select_related('customer')
    
    # Отправляем уведомления каждому клиенту
    for order in pending_orders:
        send_notification_email(
            order.customer.email,
            instance.model,
            instance.version
        )
        
def send_notification_email(email, model, version):
    """Отправка email уведомления клиенту"""
    subject = 'Робот доступен к заказу'
    message = f"""
Добрый день!

Недавно вы интересовались нашим роботом модели {model}, версии {version}. 
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
    """
    
    send_mail(
        subject=subject,
        message=message.strip(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )