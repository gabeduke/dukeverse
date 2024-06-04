from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from toolshed import views as toolshed_views  # Import views from toolshed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('toolshed.urls')),  # Adjust as needed
    path('accounts/', include('allauth.urls')),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Correct the logout URL
    # path('accounts/register/', toolshed_views.register, name='register'),  # Ensure this line is included
]
