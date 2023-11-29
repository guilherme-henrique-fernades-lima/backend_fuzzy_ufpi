from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from datetime import datetime
from integration.core.usecases.fuzzy import FuzzySystem
from integration.core.serializer import FuzzySerializer


class FuzzyViewSet(viewsets.ModelViewSet):

    # queryset = Contrato.objects.all()
    # serializer_class = ContratoMS
    permission_classes = (AllowAny,)
    serializer_class = FuzzySerializer 

    # def get_serializer_class(self):
    #     serializer = super().get_serializer_class()
    #     return serializer

    def list(self, request):

        print('Entrou dentro do metodo fuzzy')      
        # http://127.0.0.1:8005/integration/fuzzy

        try:       

            #initial_condition = request.GET.get("initial_condition", None)
            humanos_suscetiveis = request.GET.get("humanos_suscetiveis", None)
            humanos_infectados = request.GET.get("humanos_infectados", None)
            flebotomineos_suscetiveis = request.GET.get("flebotomineos_suscetiveis", None)
            flebotomineos_infectados = request.GET.get("flebotomineos_infectados", None)
            caes_suscetiveis = request.GET.get("caes_suscetiveis", None)
            caes_infectados = request.GET.get("caes_infectados", None)  

            #initial_condition = [humanos_suscetiveis, humanos_infectados, flebotomineos_suscetiveis, flebotomineos_infectados, caes_suscetiveis, caes_infectados]
            
            initial_condition = [0.7, 0, 0.24, 0.01, 0.6, 0]

            fuzzy = FuzzySystem()
            data = fuzzy.execute(initial_condition)
            
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as err:          
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
        

       


   
