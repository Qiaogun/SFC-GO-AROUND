from tabnanny import check
from django.shortcuts import render
from django.http import HttpResponse
from .models import M5sensor, Checkpoint
import json
from django.http import JsonResponse

tag_list = [1,2,3,4,5,6,7,8,9,90,10]
check_point = Checkpoint.objects.all()

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

def get_data(request):
    data = M5sensor.objects.all()
    return HttpResponse(data)

def get_postjson(request):
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
        
def cacl_point_page(request):
    data = Checkpoint.objects.all()
    if request.method == 'GET':
        return HttpResponse(data)
    return HttpResponse(data)