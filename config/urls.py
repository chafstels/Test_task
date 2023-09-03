from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static

from account.views import auth_github

schema_view = get_schema_view(
    openapi.Info(
        title="Test Task",
        default_version='v1',
        description="User account",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/account/', include('account.urls')),
    path('auth/', auth_github),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    re_path('', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
