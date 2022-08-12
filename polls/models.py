from django.db import models


class Client(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    phone = models.IntegerField(max_length=12, null=True)
    phone_code = models.IntegerField(max_length=4, null=True)
    tag = models.TextField(max_length=10, null=True)
    timezone = models.DateTimeField(auto_now_add=True)


class Mailing(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    mailing_start = models.DateTimeField()
    msg_text = models.TextField(max_length=500)
    property_filter = models.TextField(max_length=14)
    mailing_end = models.DateTimeField()


class Message(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    PRIORITIES = (
        (0, 'Отправляется'),
        (1, 'Сообщение доставлено'),
        (2, 'Error'),
    )
    msg_start = models.DateTimeField()
    msg_status = models.IntegerField(default=0, choices=PRIORITIES)
    id_mailing = models.ForeignKey('Mailing', on_delete=models.PROTECT, null=True)
    id_client = models.ForeignKey('Client', on_delete=models.PROTECT, null=True)
