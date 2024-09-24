"""
URL configuration for FitnessWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from user_auth.views import UserSignUpView, UserLoginView, UserLogoutView, FrontPageView
from notes.views import UserWorkoutsListView, DetailedWorkoutView, CreateWorkoutView, EditWorkoutView, DeleteWorkoutView, CreateWorkoutEntryView, EditWorkoutEntryView, DeleteWorkoutEntryView
from videos.views import VideoListView, VideoUploadView
from mails.views import SendMailView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserSignUpView, name="signup"),
    path('login/', UserLoginView, name="login"),
    path('logout/', UserLogoutView, name="logout"),
    path('', FrontPageView, name="frontpage"),
    path('<int:pk>/workouts', UserWorkoutsListView, name="workout_list"),
    path('<int:user_id>/workout/<int:workout_id>', DetailedWorkoutView, name="workout_detail"),
    path('<int:pk>/workouts/new', CreateWorkoutView, name="workout_create"),
    path('<int:user_id>/workout/<int:workout_id>/edit', EditWorkoutView, name="workout_edit"),
    path('<int:user_id>/workout/<int:workout_id>/delete', DeleteWorkoutView, name="workout_delete"),
    path('<int:user_id>/workout/<int:workout_id>/newentry', CreateWorkoutEntryView, name="workout_newentry"),
    path('<int:user_id>/workout/<int:workout_id>/<int:entry_id>/editentry', EditWorkoutEntryView, name="workout_editentry"),
    path('<int:user_id>/workout/<int:workout_id>/<int:entry_id>/deleteentry', DeleteWorkoutEntryView, name="workout_deleteentry"),
    path('videos/', VideoListView, name="video_list"),
    path('videos/upload', VideoUploadView, name="video_upload"),
    path('sendmail/', SendMailView, name="send_mail")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
