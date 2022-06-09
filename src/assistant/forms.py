from django import forms
from datetime import datetime
from .models import Contact, AssistantUser
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = AssistantUser
        fields = ('username', 'email')

    def save(self, commit=True):
        new_user = AssistantUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        new_user.set_password(self.cleaned_data['password1'])
        if commit:
            new_user.save()
        return new_user

    def clean(self):

        super(RegisterForm, self).clean()

        username = self.data['username']
        email = self.data['email']
        password = self.data['password1']

        all_emails = [usr.email for usr in AssistantUser.objects.all()]
        all_nicks = [usr.username for usr in AssistantUser.objects.all()]

        if username in all_nicks:
            self._errors['username'] = self.error_class(['User with this username is already having an account'])
        if len(username) > 100:
            self._errors['username'] = self.erorr_class(['Too long nickname'])
        if len(password) < 8:
            self._errors['password'] = self.error_class(['Password must be longer than 8 characters'])
        if email in all_emails:
            self._errors['email'] = self.error_class(['User with this email is already having an account'])
        if len(email) > 100:
            self._errors['email'] = self.error_class(['Too long email'])
        try:
            validate_email(email)
        except ValidationError:
            self._errors['email'] = self.error_class(['Invalid email'])

        return self.cleaned_data


class AddContact(forms.Form):
    name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'contact_name_form'}))
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'email_form'}))
    address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'address_form'}))
    phone = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'phone_form'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date_form'}))

    def clean(self):

        super(AddContact, self).clean()

        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        address = self.cleaned_data['address']
        phones = [phn.strip() for phn in self.cleaned_data['phone'].split(',')]
        birthday = self.cleaned_data['birthday']

        date_delta = (datetime.now().date() - birthday).days
        all_emails = [cnt.email for cnt in Contact.objects.all()]

        if len(name) > 40:
            self._errors['name'] = self.error_class(['Name length is maximum 40 characters'])
        if len(email) > 50:
            self._errors['email'] = self.error_class(['Email length is maximum 50 characters'])
        if email in all_emails:
            self._errors['email'] = self.error_class(['Contact with this email is already in the book'])
        if date_delta < 0:
            self._errors['birthday'] = self.error_class(['Invalid birthday'])
        if date_delta > 36525:
            self._errors['birthday'] = self.error_class(['Maximum contact age is 100 years'])
        if len(address) > 50:
            self._errors['address'] = self.error_class(['Address length is maximum 50 characters'])
        try:
            validate_email(email)
        except ValidationError:
            self._errors['email'] = self.error_class(['Invalid email'])
        if len(phones) > 4:
            self._errors['phone'] = self.error_class(['Maximum amount of phones is 4'])
        for this_phone in phones:
            if len(this_phone) > 13:
                self._errors['phone'] = self.error_class(['Phone length is maximum 13 characters'])
                break
            if not this_phone[1:].isdigit() or not this_phone.startswith('+'):
                self._errors['phone'] = self.error_class(['Phone must start with + and contain only digits'])

        return self.cleaned_data


class AddTag(forms.Form):
    tag = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'tag_form'}))

    def clean(self):

        super(AddTag, self).clean()

        tags = [tg.strip() for tg in self.cleaned_data['tag'].split(',')]

        for this_tag in tags:
            if len(this_tag) > 20:
                self._errors['tag'] = self.error_class(['Tag length is maximum 20 characters'])
                break

        return self.cleaned_data


class AddNote(forms.Form):
    note = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'note_name'}))
    description = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class': 'note_desc'}))
    tag = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'class': 'tags'}))

    def clean(self):

        super(AddNote, self).clean()

        note_to_add = self.cleaned_data['note']
        tags = [tg.strip() for tg in self.cleaned_data['tag'].split(',')]
        description = self.cleaned_data['description']

        if len(note_to_add) > 50:
            self._errors['note'] = self.error_class(['Note name length is maximum 50 characters'])
        if len(description) > 150:
            self._errors['description'] = self.error_class(['Note description length is maximum 150 characters'])
        if len(tags) > 4:
            self._errors['tag'] = self.error_class(['Maximum amount of tags is 4'])
        for this_tag in tags:
            if len(this_tag) > 20:
                self._errors['tag'] = self.error_class(['Tag length is maximum 20 characters'])
                break

        return self.cleaned_data


class ChangeName(forms.Form):
    new_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'contact_name_form'}))

    def clean(self):

        super(ChangeName, self).clean()

        new_name = self.cleaned_data['new_name']

        if len(new_name) > 40:
            self._errors['new_name'] = self.error_class(['Name length is maximum 40 characters'])

        return self.cleaned_data


class ChangeBirthday(forms.Form):
    new_birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date_form'}))

    def clean(self):

        super(ChangeBirthday, self).clean()

        new_birthday = self.cleaned_data['new_birthday']

        date_delta = (datetime.now().date() - new_birthday).days

        if date_delta < 0:
            self._errors['new_birthday'] = self.error_class(['Invalid birthday'])
        if date_delta > 36525:
            self._errors['new_birthday'] = self.error_class(['Maximum contact age is 100 years'])

        return self.cleaned_data
    
    
class AddPhone(forms.Form):
    phone = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'email_form'}))

    def clean(self):

        super(AddPhone, self).clean()

        phone = self.cleaned_data['phone']

        if len(phone) > 13:
            self._errors['phone'] = self.error_class(['Phone length is maximum 13 characters'])
        if not phone[1:].isdigit() or not phone.startswith('+'):
            self._errors['phone'] = self.error_class(['Phone must start with + and contain only digits'])

        return self.cleaned_data


class ChangeEmail(forms.Form):
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'email_form'}))

    def clean(self):

        super(ChangeEmail, self).clean()

        email = self.cleaned_data['email']

        all_emails = [cnt.email for cnt in Contact.objects.all()]

        if len(email) > 50:
            self._errors['email'] = self.error_class(['Email length is maximum 50 characters'])
        if email in all_emails:
            self._errors['email'] = self.error_class(['Contact with this email is already in the book'])
        try:
            validate_email(email)
        except ValidationError:
            self._errors['email'] = self.error_class(['Invalid email'])

        return self.cleaned_data


class ChangeAddress(forms.Form):
    new_address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'contact_name_form'}))

    def clean(self):

        super(ChangeAddress, self).clean()

        new_address = self.cleaned_data['new_address']

        if len(new_address) > 50:
            self._errors['new_address'] = self.error_class(['Address length is maximum 50 characters'])

        return self.cleaned_data
    
    
class ChangeNoteName(forms.Form):
    new_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'note_name_form'}))

    def clean(self):

        super(ChangeNoteName, self).clean()

        new_name = self.cleaned_data['new_name']

        if len(new_name) > 50:
            self._errors['new_name'] = self.error_class(['Note name length is maximum 50 characters'])

        return self.cleaned_data
    
    
class ChangeNoteDescription(forms.Form):
    new_description = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class': 'desc_note'}))

    def clean(self):

        super(ChangeNoteDescription, self).clean()

        new_description = self.cleaned_data['new_description']

        if len(new_description) > 150:
            self._errors['new_description'] = self.error_class(['Note description length is maximum 150 characters'])

        return self.cleaned_data
