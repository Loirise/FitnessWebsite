# Generated by Django 5.1 on 2024-09-25 13:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('video', models.FileField(upload_to='exercises/')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutExercises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sets', models.PositiveSmallIntegerField()),
                ('reps', models.PositiveSmallIntegerField()),
                ('weight', models.PositiveSmallIntegerField()),
                ('exercise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='notes.exercise')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.workout')),
            ],
        ),
    ]
