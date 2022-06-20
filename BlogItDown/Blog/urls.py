from os import stat
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('' , include('home.urls')),
    path('api/' , include('home.urls_api')),
    
    path('admin/', admin.site.urls),
    path('froala_editor/',include('froala_editor.urls')),

    path('oauth/', include('social_django.urls', namespace='social')),  # <-- here

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
