from django.contrib import admin
from django.urls import path,include
from . import views
app_name="Profile"
urlpatterns = [
   path('user/account/create/',views.UserProfileCreateView.as_view(),name="adduser"),
   # path('user/get/usernames/',views.UsernameRetrieveView.as_view(),name="getallusername"),
   path('user/check/username/<slug:username>/',views.ChechUsernameView.as_view(),name="checkusername"),
   path('user/account/update/',views.UserUpdateView.as_view(),name="updateuser"),
   path('user/login/',views.UserLoginView.as_view(),name="login"),
   path('user/token/refresh/',views.TokenRefreshView.as_view(),name="tokenrefresh"),
]
