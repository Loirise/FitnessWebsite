from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.title
    

class Exercise(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(max_length=50, null=False, blank=False)
    video = models.FileField(upload_to="exercises/")  # MEDIA_ROOT/exercises, for date/time add /%Y/%m/%d/

    def __str__(self):
        return self.name
    

class WorkoutExercises(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, null=True, on_delete=models.SET_NULL)
    sets = models.PositiveSmallIntegerField(null=False, blank=False)
    reps = models.PositiveSmallIntegerField(null=False, blank=False)
    weight = models.PositiveSmallIntegerField(null=False, blank=False)

    def __str__(self):
        return f"workout_id: {self.workout} - exercise_id: {self.exercise}"