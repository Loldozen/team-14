from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

from shop import views

urlpatterns = [
    path('', views.api_root),
    path('clothings/', views.ClothingList.as_view(), name='clothing-list'),
    path('clothings/<int:pk>/', views.ClothingDetail, name='clothing-detail'),
    path('clothings/<int:pk>/pay/', views.PaymentView.as_view(), name='pay'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('signup/', views.SignUpView.as_view(),name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

urlpatterns = format_suffix_patterns(urlpatterns)