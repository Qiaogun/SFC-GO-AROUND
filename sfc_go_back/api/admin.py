from django.contrib import admin
from .models import M5sensor, Checkpoint, M5sensorHeartrate
# Register your models here.

class M5dataAdmin(admin.ModelAdmin):
    list_display = ['m5tagid', 'temperature', 'humidity', 'x_axis', 'y_axis', 'z_axis', 'timestamp','ble_poi']

class CheckpointAdmin(admin.ModelAdmin):
    list_display = ['checkpointtitle', 'latitude', 'longitude', 'timestamp']

class M5sensorHeartrateAdmin(admin.ModelAdmin):
    list_display = ['m5tagid', 'heartrate', 'timestamp','ble_poi']

admin.site.register(M5sensor,M5dataAdmin)
admin.site.register(Checkpoint,CheckpointAdmin)
admin.site.register(M5sensorHeartrate,M5sensorHeartrateAdmin)