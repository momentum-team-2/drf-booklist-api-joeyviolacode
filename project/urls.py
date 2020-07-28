"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.urls import include, path
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('rest_framework.urls')),
    path('api/', api_views.api_root),
    path('api/books/', api_views.BooksList.as_view(), name="books"),
    path('api/books/<int:pk>', api_views.BookDetail.as_view(), name="book-detail"),
    path('api/note/<int:pk>', api_views.NoteDetail.as_view(), name="note-detail"),
    path('api/books/<int:pk>/notes/', api_views.NotesList.as_view(), name="notes"),
    path('api/authors/', api_views.AuthorsList.as_view(), name="authors"),
    path('api/notes/', api_views.AllNotesList.as_view(), name="all-notes"),
    path('api/timeline/<str:username>', api_views.UserTimeline.as_view(), name="timeline"),
    path('api/search/<str:query>', api_views.Search.as_view(), name="search"),
    path('api/user/timeline-setting', api_views.TimelineSetting.as_view(), name="timeline-setting"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
