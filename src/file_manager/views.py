import os
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import FileManager, FileType
from .forms import UploadFile
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, template_name='pages/index.html', context={'title': 'Web assistant'})


@login_required
def file_manager(request):
    if len(FileType.objects.all()) == 0:
        FileType.create("Video").save()
        FileType.create("Audio").save()
        FileType.create("Images").save()
        FileType.create("Archives").save()
        FileType.create("Documents").save()
        FileType.create("Other").save()
    logged_user_id = request.user.id
    files = FileManager.objects.filter(user_id=logged_user_id)
    categories = FileType.objects.all()
    list_of_names = []
    for item in files:
        list_of_names.append(str(item.file_name).split("/")[1])
    context = {
        'files': files,
        'categories': categories,
        'file_name': list_of_names,
    }

    return render(request, template_name='pages/file_manager.html', context=context)


@login_required
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="name")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def upload(request):
    logged_user_id = request.user.id
    context = {
        'form': UploadFile(),
    }
    files_types = {
        'Video': ('.avi', '.mp4', '.mov', '.mkv'),
        'Audio': ('.mp3', '.ogg', '.wav', '.amr'),
        'Images': ('.jpeg', '.png', '.jpg', '.svg'),
        'Archives': ('.zip', '.gz', '.tar'),
        'Documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    }
    if request.method == 'POST':
        file = request.FILES['file']
        file_type = Path(str(file)).suffix.lower()
        for category, extensions in files_types.items():
            if file_type in extensions:
                file_category_id = FileType.objects.get(file_type=category).id
                document = FileManager.objects.create(
                    user_id=logged_user_id,
                    file_name=file,
                    file_type_id=file_category_id,
                )
                document.save()
                return redirect('file_manager')
        other_ctg_id = FileType.objects.get(file_type='Other').id
        document = FileManager.objects.create(
            user_id=logged_user_id,
            file_name=file,
            file_type_id=other_ctg_id
        )
        document.save()
        return redirect('file_manager')
    return render(request, 'pages/upload.html', context)


@login_required
def delete_file(request, file_id):
    if FileManager.objects.get(id=file_id).user_id == request.user.id:
        FileManager.objects.get(pk=file_id).delete()
    return redirect('file_manager')


@login_required
def show_by_category(request, category_id):
    logged_user_id = request.user.id
    files = FileManager.objects.filter(user_id=logged_user_id, file_type_id=category_id)
    categories = FileType.objects.all()
    context = {
        'files': files,
        'categories': categories,
    }
    return render(request, 'pages/file_manager.html', context)
