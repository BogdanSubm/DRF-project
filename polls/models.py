import pytz
from django.core.validators import RegexValidator

from django.db import models


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone_regex = RegexValidator(regex=r'^\+7?1?\d{10}$', message="Phone number must be entered in the format: '+7XXXXXXXXXX'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=12, blank=True)
    phone_code = models.CharField(max_length=4, null=True)
    tag = models.CharField(max_length=10, null=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Mailing(models.Model):
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
