from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = "foodgram.views.page_not_found"  # noqa
handler500 = "foodgram.views.server_error"  # noqa

urlpatterns = [
    path('api/', include('api.urls')),
    path('', include('recipes.urls')),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/", include("users.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)


