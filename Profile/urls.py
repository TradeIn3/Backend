from django.contrib import admin
from django.urls import path,include
from . import views
app_name="Profile"
urlpatterns = [
   path('user/account/create/',views.UserProfileCreateView.as_view(),name="adduser"),
   path('user/check/username/<username>/',views.ChechUsernameView.as_view(),name="checkusername"),
   path('user/account/update/',views.UserUpdateView.as_view(),name="updateuser"),
   path('user/login/',views.UserLoginView.as_view(),name="login"),
   path('user/token/refresh/',views.TokenRefreshView.as_view(),name="tokenrefresh"),
   path('user/mydetails/',views.GetMyDetailsView.as_view(),name="getmydetails"),
   path('user/wishlist/',views.ProfileWishlistView.as_view(),name="userwishlist"),
   path('user/buy/',views.ProfileBuyView.as_view(),name="userbuy"),
   path('user/donate/',views.ProfileDonateView.as_view(),name="userdonate"),
   path('user/exchange/',views.ProfileExchangeView.as_view(),name="userexchange"),
   path('user/orders/',views.ProfileOrdersView.as_view(),name="userorders"),
   path('user/reserves/',views.ProfileReserveView.as_view(),name="userreserve"),
   path('user/details/',views.GetUserDetailsView.as_view(),name="userdetails"),
   path('user/image/',views.ChangeProfileImageView.as_view(),name="userimage"),
]
