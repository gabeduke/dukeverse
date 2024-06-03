from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('associate_users/', views.associate_users, name='associate_users'),
    path('assign/<int:tool_id>/', views.assign_tool, name='assign_tool'),
    path('checkin/<int:tool_id>/', views.checkin_tool, name='checkin_tool'),
    path('checkout/<int:tool_id>/', views.checkout_tool, name='checkout_tool'),
    path('create_users/', views.create_users, name='create_users'),
    path('import/', views.import_tools, name='import_tools'),
    path('register/', views.register, name='register'),
]
