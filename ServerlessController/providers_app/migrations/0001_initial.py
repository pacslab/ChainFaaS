# Generated by Django 2.2.10 on 2020-05-28 16:19

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('developers_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=datetime.datetime(2018, 7, 1, 5, 18, tzinfo=utc))),
                ('ack_time', models.DateTimeField(default=datetime.datetime(2018, 7, 1, 5, 18, tzinfo=utc))),
                ('pull_time', models.IntegerField(default=0)),
                ('run_time', models.IntegerField(default=0)),
                ('total_time', models.IntegerField(default=0)),
                ('cost', models.FloatField(default=0.0)),
                ('finished', models.BooleanField(default=False)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Provider')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='developers_app.Services')),
            ],
        ),
    ]
