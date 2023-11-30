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
           
        # http://127.0.0.1:8005/integration/fuzzy
        # http://127.0.0.1:8005/integration/fuzzy/?tempo=5&humanos_suscetiveis=0.7&humanos_infectados=0&flebotomineos_suscetiveis=0.24&flebotomineos_infectados=0.01&caes_suscetiveis=0.6&caes_infectados=0

        '''
        Condição inicial padrão da aplicação:
        initial_condition = [0.7, 0, 0.24, 0.01, 0.6, 0]         
        '''    
        try:       

            humanos_suscetiveis = request.GET.get("humanos_suscetiveis", None)
            humanos_infectados = request.GET.get("humanos_infectados", None)
            flebotomineos_suscetiveis = request.GET.get("flebotomineos_suscetiveis", None)
            flebotomineos_infectados = request.GET.get("flebotomineos_infectados", None)
            caes_suscetiveis = request.GET.get("caes_suscetiveis", None)
            caes_infectados = request.GET.get("caes_infectados", None)  
            tempo = request.GET.get("tempo", None)  

            initial_condition = [float(humanos_suscetiveis), float(humanos_infectados), float(flebotomineos_suscetiveis), float(flebotomineos_infectados), float(caes_suscetiveis), float(caes_infectados)]            
              
            fuzzy = FuzzySystem()
            data = fuzzy.execute(initial_condition, tempo)
            
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as err:          
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
        

       


   
