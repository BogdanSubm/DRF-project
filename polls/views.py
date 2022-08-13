from datetime import datetime
import json

import requests
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer
# from mailing.polls.secret import secret

secret = "asd"
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import \
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT


from .models import Client, Mailing
from .serializers import ClientSerializer, MailingSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientApiViewCreate(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            client = serializer.save()
            return Response(ClientSerializer(client).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)




class ClientApiViewUpdate(APIView):
    def get(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        serializer = ClientSerializer(client)
        return Response({'posts': serializer.data})

    def patch(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            client = serializer.save()
            return Response(ClientSerializer(client).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        client.delete()
        return Response("Клиент удалён", status=HTTP_204_NO_CONTENT)


class MailingApiViewCreate(APIView):
    def post(self, request):
        serializer = MailingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            mailing = serializer.save()
            mailing = MailingSerializer(mailing).data
            mailing_start = mailing.get('mailing_start')
            mailing_end = mailing.get('mailing_end')
            if not (mailing_start and mailing_end):
                return Response(status=HTTP_400_BAD_REQUEST)
            clients_phones = Client.objects.filter(tag=mailing.get("property_filter")).first().phone
            mailing_start = datetime.strptime(mailing_start, '%Y-%m-%dT%H:%M:%SZ')
            mailing_end = datetime.strptime(mailing_end, '%Y-%m-%dT%H:%M:%SZ')
            datetime_now = datetime.now()
            if datetime_now > mailing_start and datetime_now < mailing_end:
                headers = {
                    "Authorization": secret
                    # "accept": "application/json",
                    # "Content-Type": "application/json"
                }
                print(mailing.get("msg_text"))
                body = {
                    "id": 2,
                    "phone": 79225161025,
                    "text": mailing.get("msg_text")
                }
                response = requests.post("https://probe.fbrq.cloud/v1/send/2", headers=headers, data=json.dumps(body))
                print(response.status_code)
            return Response(mailing, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MailingApiViewUpdate(APIView):
    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        serializer = MailingSerializer(mailing)
        return Response({'posts': serializer.data})

    def patch(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        serializer = ClientSerializer(mailing, data=request.data, partial=True)
        if serializer.is_valid():
            mailing = serializer.save()
            return Response(ClientSerializer(mailing).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, mailing_id):
        client = get_object_or_404(Client, pk=mailing_id)
        client.delete()
        return Response("Рассылка удалена", status=HTTP_204_NO_CONTENT)

