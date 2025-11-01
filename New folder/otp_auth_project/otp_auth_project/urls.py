from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Mount auth_app at root so endpoints are /register/, /login/, /verify-otp/, /profile/
    path('', include('auth_app.urls')),
    # Home page (frontend)
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
]
