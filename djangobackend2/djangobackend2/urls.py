from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from api.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('api.urls')),
    path('',index)
   
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)