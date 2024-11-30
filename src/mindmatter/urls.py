from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MindMatter",
        default_version="v1",
        description="""MindMatter is a full-featured blogging platform designed to 
        provide users with an intuitive interface for creating, editing, and managing 
        blog posts. Whether you're a casual writer or a professional blogger, MindMatter
          makes it easy to share your stories, thoughts, and ideas with the world.""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="khanarfa8879@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blogs", include("blogapp.urls")),
    path("users", include("userapp.urls")),
    path("email",include("emailapp.urls")),
    path("comments", include("commentapp.urls")),
    path("", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path("silk/", include("silk.urls", namespace="silk")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
