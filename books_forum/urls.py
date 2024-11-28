"""
URL configuration for books_forum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

admin.site.site_header = 'Booklet Admin'
admin.site.site_title = 'Booklet Admin'
urlpatterns = [
    path("", include("books.urls")),
    path("", include("characters.urls")),
    path("", include("authors.urls")),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html')),
    path("", include('users.urls')),
    path("", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
