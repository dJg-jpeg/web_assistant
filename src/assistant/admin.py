from django.contrib import admin
from .models import Contact, Note, ContactPhone, NoteTag, FileManager, FileType, AssistantUser

# Register your models here.
admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(ContactPhone)
admin.site.register(NoteTag)
admin.site.register(AssistantUser)
admin.site.register(FileManager)
admin.site.register(FileType)
