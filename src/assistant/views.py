import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import Contact, Note, ContactPhone, NoteTag, FileManager
from .forms import AddContact, AddTag, AddNote, ChangeName, ChangeBirthday, AddPhone, ChangeEmail, ChangeAddress, \
    ChangeNoteName, ChangeNoteDescription


# Create your views here.
def index(request):
    return render(request, template_name='pages/index.html', context={'title': 'Web assistant'})


def contacts(request):
    phones = ContactPhone.objects.all()
    context = {'phones': phones}
    if request.method == 'POST':
        valid_contacts = []
        if 'find_contact' in request.POST:
            name = request.POST['find_contact']
            valid_contacts = Contact.objects.filter(name__icontains=name)
        elif 'find_birthday' in request.POST:
            date_interval = request.POST['find_birthday']
            try:
                date_interval = int(date_interval)
            except ValueError:
                context.update({'contact': valid_contacts})
                return render(request, template_name='pages/contact_book.html', context=context)
            for this_cnt in Contact.objects.all():
                current_date = datetime.now().date()
                this_year_birthday = datetime(
                    year=current_date.year,
                    month=this_cnt.birthday.month,
                    day=this_cnt.birthday.day,
                ).date()
                if current_date > this_year_birthday:
                    this_year_birthday = datetime(
                        year=current_date.year + 1,
                        month=this_cnt.birthday.month,
                        day=this_cnt.birthday.day,
                    ).date()
                if (this_year_birthday - current_date).days <= date_interval:
                    valid_contacts.append(this_cnt)
        context.update({'contact': valid_contacts})
    else:
        contact = Contact.objects.all()
        context.update({'contact': contact})
    return render(request, template_name='pages/contact_book.html', context=context)


def add_contact(request):
    form = AddContact()
    if request.method == 'POST':
        form = AddContact(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            birthday = form.cleaned_data['birthday']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phones = form.cleaned_data['phone']
            contact = Contact(name=name, birthday=birthday, email=email, address=address)
            contact.save()
            list_of_phones = phones.split(',')
            for phone in list_of_phones:
                added_phone = ContactPhone(contact_id=contact, phone=phone.strip())
                added_phone.save()
            return redirect('contact_book')
    return render(request, 'pages/add_contact.html', {'form': form})


def delete_contact(request, contact_id):
    Contact.objects.filter(id=contact_id).delete()
    return redirect('contact_book')


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


def delete_note(request, note_id):
    Note.objects.filter(id=note_id).delete()
    return redirect('note_book')


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


def detail_contact(request, contact_id):
    phones = ContactPhone.objects.filter(contact_id_id=contact_id)
    contact = Contact.objects.get(pk=contact_id)
    context = {
        'id_contact': contact_id,
        'phones': phones,
        'contact': contact,
    }
    return render(request, 'pages/detail_contact.html', context)


def detail_note(request, note_id):
    note_tags = NoteTag.objects.filter(note_id_id=note_id)
    note = Note.objects.get(pk=note_id)
    context = {
        'note': note,
        'tags': note_tags,
    }
    return render(request, 'pages/detail_note.html', context)


def add_phone(request, contact_id):
    context = {
        'form': AddPhone(),
        'id_contact': contact_id
    }
    if request.method == 'POST':
        context['form'] = AddPhone(request.POST)
        if context['form'].is_valid():
            phone = request.POST['phone']
            phone_to_add = ContactPhone(contact_id_id=contact_id, phone=phone.strip())
            phone_to_add.save()
            return redirect('detail_contact', contact_id=contact_id)
    return render(request, 'pages/add_phone.html', context)


def change_name(request, contact_id):
    context = {
        'form': ChangeName(),
        'id_contact': contact_id
    }
    contact = Contact.objects.get(pk=contact_id)
    if request.method == 'POST':
        context['form'] = ChangeName(request.POST)
        if context['form'].is_valid():
            new_name = request.POST['new_name']
            contact.name = new_name
            contact.save()
            return redirect('detail_contact', contact_id=contact_id)
    return render(request, 'pages/change_contact_name.html', context)


def change_email(request, contact_id):
    context = {
        'form': ChangeEmail(),
        'id_contact': contact_id
    }
    contact = Contact.objects.get(pk=contact_id)
    if request.method == 'POST':
        context['form'] = ChangeEmail(request.POST)
        if context['form'].is_valid():
            new_email = request.POST['email']
            contact.email = new_email
            contact.save()
            return redirect('detail_contact', contact_id=contact_id)
    return render(request, 'pages/change_email.html', context)


def change_birthday(request, contact_id):
    context = {
        'form': ChangeBirthday(),
        'id_contact': contact_id
    }
    contact = Contact.objects.get(pk=contact_id)
    if request.method == 'POST':
        context['form'] = ChangeBirthday(request.POST)
        if context['form'].is_valid():
            new_birthday = request.POST['new_birthday']
            contact.birthday = new_birthday
            contact.save()
            return redirect('detail_contact', contact_id=contact_id)
    return render(request, 'pages/change_birthday.html', context)


def change_address(request, contact_id):
    context = {
        'form': ChangeAddress(),
        'id_contact': contact_id
    }
    contact = Contact.objects.get(pk=contact_id)
    if request.method == 'POST':
        new_address = request.POST['new_address']
        contact.address = new_address
        contact.save()
        return redirect('detail_contact', contact_id=contact_id)
    return render(request, 'pages/change_address.html', context)


def delete_phone(request, contact_id, phone_value):
    ContactPhone.objects.filter(phone=phone_value, contact_id=contact_id).delete()
    return redirect('detail_contact', contact_id=contact_id)


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


def change_note_status(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.done = False if note.done else True
    note.save()
    return redirect('detail_note', note_id=note_id)


def delete_note_tags(request, note_id, tag_id):
    NoteTag.objects.filter(id=tag_id, note_id=note_id).delete()
    return redirect('detail_note', note_id=note_id)


def file_manager(request):
    files = FileManager.objects.all()
    list_of_files = []
    for file in files:
        list_of_files.append(os.path.basename(file.name.name))
    context = {
        'files': files,
        'files_name': list_of_files,
    }

    return render(request, template_name='pages/file_manager.html', context=context)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="name")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def upload(request):
    if request.method == 'POST':
        file_name = request.FILES['file']
        document = FileManager.objects.create(name=file_name)
        document.save()
        return redirect('file_manager')
    return render(request, 'pages/upload.html')


def delete_file(request, file_id):
    FileManager.objects.get(pk=file_id).delete()
    return redirect('file_manager')
