from django.shortcuts import render
from .forms import UploadForm


def index(request):
    return render(request, 'home/homepage.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UploadForm()
    return render(request, 'home/upload/model_form_upload.html', {"form": form})


