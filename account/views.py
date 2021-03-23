from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework import permissions

from django.http import JsonResponse, request

from .models import CustomUser

import json

class CreateUser(APIView):
    def post(self, request):
        try:
            req_post = json.loads(request.body)
            email = req_post['username']
            password = req_post['password']
            new_user = CustomUser.objects.create(email=email)
            new_user.set_password(password)
            new_user.save()
            token = Token.objects.get(user=new_user).key

            data = {
                'token': token,
                'user': {
                    'email': new_user.email
                }
            }

            return JsonResponse(data, safe=False)

        except:
            return JsonResponse(status=400, data={'message': 'email already registered'}, safe=False)
