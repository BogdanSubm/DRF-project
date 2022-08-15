from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Client, Mailing, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ClientSerializer(serializers.Serializer):
    phone = serializers.CharField()
    phone_code = serializers.CharField()
    tag = serializers.CharField()
    timezone = serializers.CharField()

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class MailingSerializer(serializers.Serializer):
    mailing_start = serializers.DateTimeField()
    msg_text = serializers.CharField()
    tag = serializers.CharField()
    mailing_end = serializers.DateTimeField()

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        return Mailing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


# class MessageSerializer(serializers.Serializer):
#     msg_start = serializers.DateTimeField()
#     msg_status = serializers.IntegerField()
#     id_mailing = serializers.CharField()
#     id_client = serializers.CharField()
#
#     class Meta:
#         model = Message
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return Message.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance
