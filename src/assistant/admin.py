from django.contrib import admin
from .models import Contact, Note, ContactPhone, NoteTag, FileManager

# Register your models here.
admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(ContactPhone)
admin.site.register(NoteTag)
admin.site.register(FileManager)
