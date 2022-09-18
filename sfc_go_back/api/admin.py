from django.contrib import admin
from .models import M5sensor, Checkpoint
# Register your models here.

class M5dataAdmin(admin.ModelAdmin):
    list_display = ['m5tagid', 'temperature', 'humidity', 'x_axis', 'y_axis', 'z_axis', 'timestamp']

class CheckpointAdmin(admin.ModelAdmin):
    list_display = ['checkpointtitle', 'latitude', 'longitude', 'timestamp']

admin.site.register(M5sensor,M5dataAdmin)
admin.site.register(Checkpoint,CheckpointAdmin)