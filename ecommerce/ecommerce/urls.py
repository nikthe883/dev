
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [

    # Admin url
    
    path('admin/', admin.site.urls),

    
    # Store app

    path('', include('store.urls')),


    # Account app

    path('account/', include('account.urls')),

    # Message app

    path('messaging/', include('messaging.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


