from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('upload_folder/', views.upload_folder, name='upload_folder'),
    path('', include('django.contrib.auth.urls')),
    path('files/', include('db_file_storage.urls')),
    url(r'^delete/(.*)/$', views.delete, name='delete'),
    path('deadlocksf/', views.deadlocksetfalse, name='deadlocksf'),
    path('deadlockst/', views.deadlocksettrue, name='deadlockst')
]
