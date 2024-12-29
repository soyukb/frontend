from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

# Create your views here.
class ItemView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self,request):
        return Response({'method':'get'})