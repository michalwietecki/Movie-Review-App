"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from general.views import base_screen_view
from account.views import registration_view, logout_view, login_view, activate_account
from reviews.views import (movie_detail, create_review_ajax, reviews_api, your_reviews_view, delete_review, edit_review,
                           search_results_view)
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", base_screen_view, name="home"),
    path("register/", registration_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('movie/<slug:slug>/', movie_detail, name='movie_detail'),
    path('movie/<slug:slug>/create-review/', create_review_ajax, name='create_review_ajax'),
    path('api/reviews/<slug:slug>/', reviews_api, name='reviews_api'),
    path('review/<int:review_id>/delete/', delete_review, name='delete_review'),
    path('review/<int:review_id>/edit/', edit_review, name='edit_review'),
    path('your_reviews/', your_reviews_view, name='your_reviews'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('activation_complete/', activate_account, name='activate_account'),
    path('search/', search_results_view, name='search_results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)