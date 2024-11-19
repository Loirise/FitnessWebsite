from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import VideoModel
from django.contrib.auth.models import Permission

# Create your views here.

def VideoListView(request):
    has_perms = request.user.groups.filter(name='Staff').exists()
    if request.user.is_authenticated and request.user.has_perm('videos.view_videomodel'):
        posts = VideoModel.objects.all()
        return render(request, "video_list.html", {'posts': posts, 'has_perms': has_perms})
    # not logged in
    return redirect("frontpage")

def VideoUploadView(request):

    if request.user.is_authenticated and request.user.has_perm('videos.add_videomodel'):
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                instance = VideoModel(title=request.POST.get('title'), video=request.FILES.get('file'))
                instance.save()
                return redirect("video_list")
        else:
            form = VideoForm()
        return render(request, "video_upload.html", {'form':form})
    # not logged in
    return redirect("frontpage")


#todo: messages for "if not logged in"
