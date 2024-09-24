from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Workout, Exercise, WorkoutExercises
from .forms import CreateWorkoutForm, CreateWorkoutEntryForm

# Create your views here.

def UserWorkoutsListView(request, pk):

    # checks if user is logged in and if logged in user is requesting
    if request.user.is_authenticated and request.user.id == pk:
        # get user by id, also get user workouts
        user = User.objects.filter(id=pk)[0]
        workouts = Workout.objects.filter(user=user.id)
        return render(request, "workout_list.html", {"workouts": workouts, "user_id": pk})
    else:
        # not logged in
        return redirect("login")
    

def DetailedWorkoutView(request, user_id, workout_id):

    # checks if user is logged in and if logged in user is requesting
    if request.user.is_authenticated and request.user.id == user_id:
        # get workouts details - title/exercises/sets/reps/weight
        title = Workout.objects.filter(id=workout_id)[0]
        workout_exercises = WorkoutExercises.objects.values().filter(workout=workout_id)
        workout_exercises_ids = [workout_exercises[i]["id"] for i in range(len(workout_exercises))]
        exercise = [Exercise.objects.filter(id=workout_exercises[i]["exercise_id"])[0] for i in range(len(workout_exercises))]
        sets = [workout_exercises[i]["sets"] for i in range(len(workout_exercises))]
        reps = [workout_exercises[i]["reps"] for i in range(len(workout_exercises))]
        weight = [workout_exercises[i]["weight"] for i in range(len(workout_exercises))]
        context = {
            "exercises": zip(workout_exercises_ids, exercise, sets, reps, weight),
            "workout_id": workout_id,
            "title": title,
            "user_id": user_id,
            "workout_id": workout_id 
        }
        return render(request, "workout_details.html", context)
    else:
        # not logged in
        return redirect("login")
    

def CreateWorkoutView(request, pk):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateWorkoutForm(request.POST)
            # update form with users id
            updated_data = request.POST.copy()
            updated_data.update({"user": pk})
            form = CreateWorkoutForm(data=updated_data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse_lazy("workout_list", kwargs={'pk': pk}))
        else:
            form = CreateWorkoutForm()
    else:
        # not logged in
        return redirect("login")
            
    return render(request, "workout_create.html", {'form': form, 'user_id': pk})


def EditWorkoutView(request, user_id, workout_id):

    # get workout by id
    workout = Workout.objects.filter(id=workout_id)[0]
    # checks if user is logged in and if logged in user is requesting
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == "POST":
            form = CreateWorkoutForm(request.POST)
            # update form with users id
            updated_data = request.POST.copy()
            updated_data.update({"user": user_id})
            form = CreateWorkoutForm(data=updated_data)
            if form.is_valid():
                form.edit(workout_id)
                return HttpResponseRedirect(reverse_lazy("workout_list", kwargs={'pk': user_id}))
        else:
            form = CreateWorkoutForm(data={'title': workout.title, 'date': workout.date})
    else:
        # not logged in
        return redirect("login")

    return render(request, "workout_edit.html", {'form': form, 'user_id': user_id})


def DeleteWorkoutView(request, user_id, workout_id):

    workout = Workout.objects.filter(id=workout_id)[0]
    # checks if user is logged in and if logged in user is requesting
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == "POST":
            workout.delete()
            return HttpResponseRedirect(reverse_lazy("workout_list", kwargs={'pk': user_id}))
    else:
        # not logged in
        return redirect("login")
    
    return render(request, "workout_delete.html", {'workout': workout, 'user_id': user_id})


def CreateWorkoutEntryView(request, user_id, workout_id):

    #get all exercises and its ids
    exercises = [(id, exer, ctgy, vid) for id, exer, ctgy, vid in list(Exercise.objects.values_list())]

    # checks if user is logged in and if logged in user is requesting
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == "POST":
            form = CreateWorkoutEntryForm(request.POST)
            updated_data = request.POST.copy()
            #adds workout id to the form
            updated_data.update({'workout': workout_id})
            form = CreateWorkoutEntryForm(data=updated_data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse_lazy("workout_detail", kwargs={'user_id': user_id, 'workout_id': workout_id}))
        else:
            form = CreateWorkoutEntryForm()
    else:
        # not logged in
        return redirect("login")
    return render(request, "workout_entry_create.html", {'form': form, 'exercises': exercises, 'pk': user_id})


def EditWorkoutEntryView(request, user_id, workout_id, entry_id):

    # get workout by id and list of all exercises
    workoutentry = WorkoutExercises.objects.filter(id=entry_id)[0]
    exercises = [(id, exer, ctgy, vid) for id, exer, ctgy, vid in list(Exercise.objects.values_list())]
    # checks if user is logged in and if logged in user is requesting
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == "POST":
            form = CreateWorkoutEntryForm(request.POST)
            # update form with users id and workout id
            updated_data = request.POST.copy()
            updated_data.update({"user": user_id, "workout": workout_id})
            form = CreateWorkoutEntryForm(data=updated_data)
            if form.is_valid():
                form.edit(entry_id)
                return HttpResponseRedirect(reverse_lazy("workout_detail", kwargs={'user_id': user_id, 'workout_id':workout_id}))
        else:
            form = CreateWorkoutEntryForm(data={'exercise':  workoutentry.exercise, 
                                                'sets':  workoutentry.sets,
                                                'reps':  workoutentry.reps,
                                                'weight':  workoutentry.weight})
    else:
        # not logged in
        return redirect("login")

    return render(request, "workout_entry_edit.html", {'form': form, 'user_id': user_id, 'workout_id': workout_id, 'exercises': exercises})


def DeleteWorkoutEntryView(request, user_id, workout_id, entry_id):

    workout_entry = WorkoutExercises.objects.filter(id=entry_id)[0]
    # checks if user is logged in and if logged in user is requesting
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == "POST":
            workout_entry.delete()
            return HttpResponseRedirect(reverse_lazy("workout_detail", kwargs={'user_id': user_id, 'workout_id':workout_id}))
    else:
        # not logged in
        return redirect("login")
    
    return render(request, "workout_entry_delete.html", {'entry': workout_entry, 'user_id': user_id, 'workout_id': workout_id})

#need jquery plugin if want to filter through dropdown
