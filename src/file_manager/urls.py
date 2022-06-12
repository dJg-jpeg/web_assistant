from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('file_manager/', views.file_manager, name='file_manager'),
    path('file_manager/upload/', views.upload, name='upload'),
    path('file_manager/delete_file/<file_id>', views.delete_file, name='delete_file'),
    path('file_manager/show_by_category/<category_id>', views.show_by_category, name='show_by_category'),
    url(r'^download/(?P<path>.*)$/', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
