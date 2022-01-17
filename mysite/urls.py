
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),   #URL namespaces allow you to uniquely reverse named URL patterns 
]
