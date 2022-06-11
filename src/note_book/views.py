from django.shortcuts import render, redirect
from .models import Note, NoteTag
from .forms import AddTag, AddNote, ChangeNoteName, ChangeNoteDescription
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, template_name='pages/index.html', context={'title': 'Web assistant'})


@login_required
def notes(request):
    all_notes = Note.objects.all()
    note_tags = NoteTag.objects.all()
    context = {
        'notes': all_notes,
        'tags': note_tags,
    }
    if request.method == 'POST':
        if 'find_note' in request.POST:
            name = request.POST['find_note']
            context.update({'notes': Note.objects.filter(name__icontains=name)})
        elif 'find_by_tag' in request.POST:
            notes_with_tags = request.POST['find_by_tag']
            tags = NoteTag.objects.filter(tag__icontains=notes_with_tags)
            context.update({"tags": tags})
            contacts_with_id = []
            for item in tags:
                if item.note_id_id not in contacts_with_id:
                    contacts_with_id.append(item.note_id_id)
            valid_notes = []
            for item in contacts_with_id:
                valid_notes.append(Note.objects.get(pk=item))
            context.update({'notes': valid_notes})

    return render(request, template_name='pages/notes.html', context=context)


@login_required
def delete_note(request, note_id):
    Note.objects.filter(id=note_id).delete()
    return redirect('note_book')


@login_required
def add_tag(request, note_id):
    context = {
        'form': AddTag(),
        'id_note': note_id,
    }
    if request.method == "POST":
        context['form'] = AddTag(request.POST)
        if context['form'].is_valid():
            new_tag_value = context['form'].cleaned_data['tag']
            new_tag = NoteTag(tag=new_tag_value, note_id=Note.objects.filter(id=note_id)[0])
            new_tag.save()
            return redirect('detail_note', note_id=note_id)
    return render(request, 'pages/add_tag.html', context)


@login_required
def add_note(request):
    context = {
        'form': AddNote(),
    }
    if request.method == 'POST':
        context['form'] = AddNote(request.POST)
        if context['form'].is_valid():
            note = context['form'].cleaned_data['note']
            tags = context['form'].cleaned_data['tag']
            description = context['form'].cleaned_data['description']
            note_to_db = Note(name=note, description=description)
            note_to_db.save()
            list_of_tags = tags.split(',')
            for tag in list_of_tags:
                tag_to_db = NoteTag(tag=tag.strip(), note_id=note_to_db)
                tag_to_db.save()
            return redirect('note_book')
    return render(request, 'pages/add_note.html', context)


@login_required
def detail_note(request, note_id):
    note_tags = NoteTag.objects.filter(note_id_id=note_id)
    note = Note.objects.get(pk=note_id)
    context = {
        'note': note,
        'tags': note_tags,
    }
    return render(request, 'pages/detail_note.html', context)


@login_required
def change_note_name(request, note_id):
    context = {
        'form': ChangeNoteName(),
        'note_id': note_id
    }
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        context['form'] = ChangeNoteName(request.POST)
        if context['form'].is_valid():
            new_name = request.POST['new_name']
            note.name = new_name
            note.save()
            return redirect('detail_note', note_id=note_id)
    return render(request, 'pages/change_note_name.html', context)


@login_required
def change_note_description(request, note_id):
    context = {
        'form': ChangeNoteDescription(),
        'note_id': note_id
    }
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        context['form'] = ChangeNoteDescription(request.POST)
        if context['form'].is_valid():
            new_description = request.POST['new_description']
            note.description = new_description
            note.save()
            return redirect('detail_note', note_id=note_id)
    return render(request, 'pages/change_note_description.html', context)


@login_required
def change_note_status(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.done = False if note.done else True
    note.save()
    return redirect('detail_note', note_id=note_id)


@login_required
def delete_note_tags(request, note_id, tag_id):
    NoteTag.objects.filter(id=tag_id, note_id=note_id).delete()
    return redirect('detail_note', note_id=note_id)