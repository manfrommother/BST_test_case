from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime
from .models import Robot

@method_decorator(csrf_exempt, name='dispatch')
class RobotCreateView(View):
    """Представление для создания робота через API"""
    
    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса для создания робота"""
        try:
            data = json.loads(request.body)
            
            # Проверяем длину модели
            if len(data.get('model', '')) != 2:
                return JsonResponse(
                    {'error': 'Model must be exactly 2 characters long'}, 
                    status=400
                )
                
            # Проверяем длину версии
            if len(data.get('version', '')) != 2:
                return JsonResponse(
                    {'error': 'Version must be exactly 2 characters long'}, 
                    status=400
                )
                
            # Проверяем дату
            try:
                created = datetime.strptime(data['created'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, KeyError):
                return JsonResponse(
                    {'error': 'Invalid datetime format. Use YYYY-MM-DD HH:MM:SS'}, 
                    status=400
                )
            
            # Создаем робота
            robot = Robot.objects.create(
                model=data['model'],
                version=data['version'],
                created=created
            )
            
            return JsonResponse({
                'model': robot.model,
                'version': robot.version,
                'created': robot.created.strftime("%Y-%m-%d %H:%M:%S")
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON format'}, 
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=500
            )
