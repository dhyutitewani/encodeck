from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('encrypter', views.encrypter, name='encrypter'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('decrypter', views.decrypter, name='decrypter'),   
    path('decrypter/<int:file_id>/', views.decrypter, name='decrypt_file'), 
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('download_file/<int:file_id>/<str:file_type>/', views.download_file, name='download_file'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)