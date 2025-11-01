"""
URL configuration for forms_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from forms_app.views import (
    UserViewSet,
    FormularViewSet,
    FilledFormViewSet,
    QuestionViewSet,
    OptionViewSet,
    register_user,
    login_user,
    logout_user,
)

# Router za API viewsetove
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'forms', FormularViewSet)
router.register(r'filled_forms', FilledFormViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)

urlpatterns = [
    # 🏠 Početna (index.html iz frontend foldera)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # 🔹 Frontend stranice (HTML fajlovi)
    path('forms/', TemplateView.as_view(template_name='view_forms.html'), name='view_forms'),
    path('form_editor/', TemplateView.as_view(template_name='form_editor.html'), name='form_editor'),
    path('results/', TemplateView.as_view(template_name='results.html'), name='results'),
   path('fill_form/', TemplateView.as_view(template_name='fill_form.html'), name='fill_form'),


    # 🔹 Admin
    path('admin/', admin.site.urls),

    # 🔹 Custom auth endpointi (backend)
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # 🔹 API CRUD rute
    path('api/', include(router.urls)),

    # 🔹 JWT tokeni (za login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Staticki fajlovi (CSS/JS/slike) i media (upload)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
