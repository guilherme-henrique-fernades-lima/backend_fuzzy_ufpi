from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from datetime import datetime
from integration.core.usecases.fuzzy import FuzzySystem
from integration.core.serializer import FuzzySerializer

class FuzzyViewSet(viewsets.ModelViewSet):

    permission_classes = (AllowAny,)
    serializer_class = FuzzySerializer  

    def list(self, request):
           
        try:       

            humanos_suscetiveis = request.GET.get("humanos_suscetiveis", None)
            humanos_infectados = request.GET.get("humanos_infectados", None)
            flebotomineos_suscetiveis = request.GET.get("flebotomineos_suscetiveis", None)
            flebotomineos_infectados = request.GET.get("flebotomineos_infectados", None)
            caes_suscetiveis = request.GET.get("caes_suscetiveis", None)
            caes_infectados = request.GET.get("caes_infectados", None)  
            tempo = request.GET.get("tempo", None)  
            encoleiramento_caes_suscetiveis = request.GET.get("encoleiramento_caes_suscetiveis", None)  
            encoleiramento_caes_infectados = request.GET.get("encoleiramento_caes_infectados", None)  
            gamma_c = request.GET.get("gamma_c", None)  

            initial_condition = [
                float(humanos_suscetiveis), 
                float(humanos_infectados), 
                float(flebotomineos_suscetiveis), 
                float(flebotomineos_infectados), 
                float(caes_suscetiveis), 
                float(caes_infectados),                
                float(encoleiramento_caes_suscetiveis),  
                float(encoleiramento_caes_infectados)
            ]     
              
            fuzzy = FuzzySystem()
            data = fuzzy.execute(initial_condition, tempo, float(gamma_c))
            
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as err:          
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
        

       


   
