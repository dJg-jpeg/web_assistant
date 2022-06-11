from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Contact, ContactPhone
from .forms import AddContact, ChangeName, ChangeBirthday, AddPhone, ChangeEmail, ChangeAddress


# Create your views here.
def index(request):
    return render(request, template_name='pages/index.html', context={'title': 'Web assistant'})


@login_required
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


@login_required
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


@login_required
def delete_contact(request, contact_id):
    Contact.objects.filter(id=contact_id).delete()
    return redirect('contact_book')


@login_required
def detail_contact(request, contact_id):
    phones = ContactPhone.objects.filter(contact_id_id=contact_id)
    contact = Contact.objects.get(pk=contact_id)
    context = {
        'id_contact': contact_id,
        'phones': phones,
        'contact': contact,
    }
    return render(request, 'pages/detail_contact.html', context)


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def delete_phone(request, contact_id, phone_value):
    ContactPhone.objects.filter(phone=phone_value, contact_id=contact_id).delete()
    return redirect('detail_contact', contact_id=contact_id)
