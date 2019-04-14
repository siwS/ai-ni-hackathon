from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("record/", hello.views.record, name="record"),
    path("upload/", hello.views.upload, name="upload"),
    path("audio/", hello.views.audio, name="audio"),
    path("about-us/", hello.views.aboutUs, name="about-us"),

    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
