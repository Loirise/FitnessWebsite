from django import forms
from .models import Workout, Exercise, WorkoutExercises
from django.contrib.auth.models import User

class CreateWorkoutForm(forms.Form):
    user = forms.IntegerField(required=True)
    title = forms.CharField(required=True, max_length=100)
    date = forms.DateField(required=True)

    def save(self, commit=True):
        user = User.objects.filter(id=self.cleaned_data["user"])[0]
        workout = Workout(
            user = user,
            title = self.cleaned_data["title"],
            date = self.cleaned_data["date"]
        )
        workout.save()
        return workout
    
    def edit(self, id, commit=True):
        workout = Workout.objects.filter(id=id)[0]
        workout.title = self.cleaned_data["title"]
        workout.date = self.cleaned_data["date"]
        workout.save()
        return workout

class CreateWorkoutEntryForm(forms.Form):
    workout = forms.IntegerField(required=True, widget=forms.HiddenInput())
    exercise = forms.ModelChoiceField(required=True, queryset=Exercise.objects.values())
    sets = forms.IntegerField(required=True)
    reps = forms.IntegerField(required=True)
    weight = forms.IntegerField(required=True)

    def save(self, commit=True):
        workout = Workout.objects.filter(id=self.cleaned_data['workout'])[0]
        exercise = Exercise.objects.filter(id=self.cleaned_data['exercise']['id'])[0]
        entry = WorkoutExercises(
            workout = workout,
            exercise = exercise,
            sets = int(self.cleaned_data['sets']),
            reps = int(self.cleaned_data['reps']),
            weight = int(self.cleaned_data['weight'])
        )
        entry.save()
        return entry
    
    def edit(self, id, commit=True):
        workoutentry = WorkoutExercises.objects.filter(id=id)[0]
        workoutentry.exercise = Exercise.objects.filter(id=self.cleaned_data['exercise']['id'])[0]
        workoutentry.sets = int(self.cleaned_data['sets'])
        workoutentry.reps = int(self.cleaned_data['reps'])
        workoutentry.weight = int(self.cleaned_data['weight'])
        workoutentry.save()
        return workoutentry
