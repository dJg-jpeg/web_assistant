from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact_book/', views.contacts, name='contact_book'),
    path('contact_book/add_contact/', views.add_contact, name='add_contact'),
    path('contact_book/del_contact/<contact_id>', views.delete_contact, name='delete_contact'),
    path('contact_book/detail/<contact_id>', views.detail_contact, name='detail_contact'),
    path('contact_book/change_name/<contact_id>', views.change_name, name='change_name'),
    path('contact_book/change_birthday/<contact_id>', views.change_birthday, name='change_birthday'),
    path('contact_book/add_phone/<contact_id>', views.add_phone, name='add_phone'),
    path('contact_book/detail/<contact_id>/delete_phone/<phone_value>', views.delete_phone, name='delete_phone'),
    path('contact_book/change_email/<contact_id>/', views.change_email, name='change_email'),
    path('contact_book/change_address/<contact_id>/', views.change_address, name='change_address'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
