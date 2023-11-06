from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #Direcionamento pra aplicação
    path('', include('app.urls')),
]