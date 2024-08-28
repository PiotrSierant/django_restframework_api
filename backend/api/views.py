import os
from dotenv import load_dotenv
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, NipSerializer
from litex.regon import REGONAPI
from lxml import etree
from .utils.xml_to_json import xml_string_to_json

load_dotenv()

class CreateUserView(generics.CreateAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class NipView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nip):
        serializer = NipSerializer(data={'nip': nip})

        if serializer.is_valid():

            # Inicjalizacja API REGON
            api = REGONAPI(os.getenv('REGON_SERVICE_URL'))
            api.login(os.getenv('REGON_USER_KEY'))

            try:
                entities = api.search(nip=nip, detailed=False)
                if entities:
                    xml_strings = [etree.tostring(entity, pretty_print=True).decode() for entity in entities]
                    json_strings = [xml_string_to_json(xml_string) for xml_string in xml_strings]

                    return Response( '\n'.join(json_strings), content_type='application/json')
                    
                else:
                    return Response({'error': 'Brak wyników dla podanego NIP'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                # Obsługa błędów podczas komunikacji z API REGON
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Jeśli numer NIP jest niepoprawny, zwróć błąd
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        