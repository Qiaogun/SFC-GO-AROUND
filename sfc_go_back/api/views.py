from re import M
from tabnanny import check
from django.shortcuts import render
from django.http import HttpResponse
from .models import M5sensor, Checkpoint, M5sensorHeartrate
import json
from django.http import JsonResponse

def get_checkpoint_taglist():
    res = []
    checkpoint_list = Checkpoint.objects.all()
    for i in checkpoint_list:
        res.append(i.checkpointtitle)
    return res

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

def get_data(request):
    data = M5sensor.objects.all()
    return HttpResponse(data)

def get_env3json(request):
    if request.method == 'POST':
        postbody = request.body
        postbody = postbody.decode('utf-8')
        postbody = json.loads(postbody)
        print(postbody)
        m5tagid = postbody['m5tagid']
        temperature = postbody['temperature']
        humidity = postbody['humidity']
        x_axis = postbody['x_axis']
        y_axis = postbody['y_axis']
        z_axis = postbody['z_axis']
        timestamp = postbody['timestamp']
        ble_poi = postbody['BLE']
        m5sensor = M5sensor.create(m5tagid, temperature, humidity, x_axis, y_axis, z_axis, timestamp, ble_poi)
        m5sensor.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("Not OK")

def get_heartratejson(request):
    if request.method == 'POST':
        postbody = request.body
        postbody = postbody.decode('utf-8')
        postbody = json.loads(postbody)
        print(postbody)
        m5tagid = postbody['m5tagid']
        heartrate = postbody['heartrate']
        timestamp = postbody['timestamp']
        ble_poi = postbody['BLE']
        m5sensor = M5sensorHeartrate.create(m5tagid, heartrate, timestamp, ble_poi)
        m5sensor.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("Not OK")

def cacl_point_page(request,time_start,time_end):
    tagelist = get_checkpoint_taglist()
    if request.method == 'GET':
        M5sensor_list = M5sensor.objects.filter(timestamp__range=(time_start, time_end))
        M5sensorHeartrate_list = M5sensorHeartrate.objects.filter(timestamp__range=(time_start, time_end))
        for i in  tagelist: 
            return HttpResponse(200)
    if request.method == 'GET':
        return HttpResponse(200)
    return HttpResponse(200)