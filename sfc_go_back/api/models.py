from tabnanny import check
from this import d
from django.db import models

# Create your models here.

class M5sensor(models.Model):
    m5tagid = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    x_axis = models.FloatField()
    y_axis = models.FloatField()
    z_axis = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ble_poi = models.CharField(max_length=100, default='')

    @classmethod
    def create(cls, m5tagid, temperature, humidity, x_axis, y_axis, z_axis, timestamp, ble_poi):
        m5sensor = cls(m5tagid=m5tagid, temperature=temperature, humidity=humidity, x_axis=x_axis, y_axis=y_axis, z_axis=z_axis, timestamp=timestamp, ble_poi=ble_poi)
        return m5sensor

class M5sensorHeartrate(models.Model):
    m5tagid = models.CharField(max_length=100)
    heartrate = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    ble_poi = models.CharField(max_length=100)

    @classmethod
    def create(cls, m5tagid, heartrate, timestamp, ble_poi):
        m5sensor = cls(m5tagid=m5tagid, heartrate=heartrate, timestamp=timestamp, ble_poi=ble_poi)
        return m5sensor

class Checkpoint(models.Model):
    bleid = models.CharField(max_length=100)
    checkpointid = models.CharField(max_length=100)
    checkpointtitle = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

