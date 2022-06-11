from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('note_book/add_note', views.add_note, name='add_note'),
    path('note_book/', views.notes, name='note_book'),
    path('note_book/del_note/<note_id>', views.delete_note, name='delete_note'),
    path('contact_book/note_book/add_tag/<note_id>', views.add_tag, name='add_tag'),
    path('note_book/detail_note/<note_id>', views.detail_note, name='detail_note'),
    path('note_book/change_note/<note_id>', views.change_note_name, name='change_note_name'),
    path('note_book/change_note_description/<note_id>', views.change_note_description, name='change_note_description'),
    path('note_book/change_note_status/<note_id>', views.change_note_status, name='change_note_status'),
    path('note_book/note_detail/<note_id>/delete_tag/<tag_id>', views.delete_note_tags, name='delete_note_tags'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
