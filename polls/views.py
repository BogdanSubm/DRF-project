from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT


from .models import Client, Mailing, Message
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
        print(serializer.data)
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
            return Response(ClientSerializer(mailing).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MailingApiViewUpdate(APIView):
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

