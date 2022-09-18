# Generated by Django 4.1.1 on 2022-09-18 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_m5sensor_ble_poi'),
    ]

    operations = [
        migrations.CreateModel(
            name='M5sensorHeartrate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m5tagid', models.CharField(max_length=100)),
                ('heartrate', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ble_poi', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='checkpoint',
            name='bleid',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='m5sensor',
            name='ble_poi',
            field=models.CharField(default='', max_length=100),
        ),
    ]