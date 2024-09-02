from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', register_user, name='register'),
    path('user-logout', user_logout, name='user_logout'),
    path('', home, name='home'),
    path('query-builder', query_builder, name='query_builder'),
    path('query', login_required(Query_Builder.as_view())),
    path('add-user', login_required(UserRegistrationView.as_view()), name='add_user'),
    path('all-users', login_required(Show_user.as_view()), name='show_users'),
    path('delete-user/<int:id>', delete_user, name='delete_user'),
]
