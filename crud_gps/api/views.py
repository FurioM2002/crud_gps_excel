from typing import Any
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse as HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Posicion
import json

# Create your views here.
#Creación de Views para el modelo Posicion
class PosicionView(View):
    
    #Def para anular token CSRF (Para autorizar inserciones)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    #Creación de Request GET (Posicion)
    """def get(self, request):
        posiciones = Posicion.objects.all()
        data=[]
        
        for posicion in posiciones:
            posicion_data = {
                "imei": posicion.imei,
                "position": {
                    "lat": posicion.lat,
                    "lon": posicion.lon
                },
                "alt": posicion.alt,
                "speed": posicion.speed,
                "orientation": posicion.orientation,
                "sensores": {
                    "acc": posicion.acc,
                    "dil": posicion.dil,
                    "towing": posicion.towing
                    
                }
            }
            data.append(posicion_data)
            
        response_data = {
            "message": "Datos listados con éxito",
            "posiciones": data
        }
        
        return JsonResponse(response_data)"""
    
    def get(self, request, posicion_id=None):
        if posicion_id is None:
            # Listar todos los registros
            posiciones = Posicion.objects.all()
        else:
            # Listar un registro específico por ID
            try:
                posiciones = Posicion.objects.filter(id=posicion_id)
            except Posicion.DoesNotExist:
                response_data = {
                    "message": f"No se encontró la posición con ID {posicion_id}",
                    "posiciones": []
                }
                return JsonResponse(response_data, status=404)

        data = []

        for posicion in posiciones:
            posicion_data = {
                "imei": posicion.imei,
                "position": {
                    "lat": posicion.lat,
                    "lon": posicion.lon
                },
                "alt": posicion.alt,
                "speed": posicion.speed,
                "orientation": posicion.orientation,
                "sensores": {
                    "acc": posicion.acc,
                    "dil": posicion.dil,
                    "towing": posicion.towing
                }
            }
            data.append(posicion_data)

        if posicion_id is None:
            # Si no se proporciona un ID, listar todos los registros
            response_data = {
                "message": "Datos listados con éxito",
                "posiciones": data
            }
        else:
            # Si se proporciona un ID, listar el registro específico
            response_data = {
                "message": f"Dato listado con éxito para la posición con ID {posicion_id}",
                "posiciones": data
            }

        return JsonResponse(response_data)
    
    #Creacion de Request POST (Posicion)
    def post(self, request):
        data=json.loads(request.body)
        Posicion.objects.create(imei=data['imei'], lat=data['lat'], lon=data['lon'], alt=data['alt'], speed=data['speed'], orientation=data['orientation'], acc=data['acc'], dil=data['dil'], towing=data['towing'])
        response_data = {
            "message": "Datos guardados con éxito"
        }
        return JsonResponse(response_data)
    
    
