from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('contact_book/', views.contacts, name='contact_book'),
    path('contact_book/add_contact/', views.add_contact, name='add_contact'),
    path('note_book/add_note', views.add_note, name='add_note'),
    path('contact_book/del_contact/<contact_id>', views.delete_contact, name='delete_contact'),
    path('note_book/', views.notes, name='note_book'),
    path('note_book/del_note/<note_id>', views.delete_note, name='delete_note'),
    path('contact_book/note_book/add_tag/<note_id>', views.add_tag, name='add_tag'),
    path('contact_book/detail/<contact_id>', views.detail_contact, name='detail_contact'),
    path('note_book/detail_note/<note_id>', views.detail_note, name='detail_note'),
    path('contact_book/change_name/<contact_id>', views.change_name, name='change_name'),
    path('contact_book/change_birthday/<contact_id>', views.change_birthday, name='change_birthday'),
    path('contact_book/add_phone/<contact_id>', views.add_phone, name='add_phone'),
    path('contact_book/detail/<contact_id>/delete_phone/<phone_value>', views.delete_phone, name='delete_phone'),
    path('contact_book/change_email/<contact_id>/', views.change_email, name='change_email'),
    path('contact_book/change_address/<contact_id>/', views.change_address, name='change_address'),
    path('note_book/change_note/<note_id>', views.change_note_name, name='change_note_name'),
    path('note_book/change_note_description/<note_id>', views.change_note_description, name='change_note_description'),
    path('note_book/change_note_status/<note_id>', views.change_note_status, name='change_note_status'),
    path('note_book/note_detail/<note_id>/delete_tag/<tag_id>', views.delete_note_tags, name='delete_note_tags'),
    path('file_manager/', views.file_manager, name='file_manager'),
    path('file_manager/upload/', views.upload, name='upload'),
    path('file_manager/delete_file/<file_id>', views.delete_file, name='delete_file'),
    path('file_manager/show_by_category/<category_id>', views.show_by_category, name='show_by_category'),
    url(r'^download/(?P<path>.*)$/', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
