from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# from integration.core.models import Contrato
# from integration.core.serializer import ContratoMS

import pandas as pd
from datetime import datetime, timedelta


class FuzzyViewSet(viewsets.ModelViewSet):

    # queryset = Contrato.objects.all()
    # serializer_class = ContratoMS
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer

    def list(self, request):
        print('Entrou dentro do metodo fuzzy')      

        # try:         
        #   return Response(data=data, status=status.HTTP_200_OK)

        # except Exception as err:          
        #     return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

   
