from django.contrib import admin
from django.urls import path,include
from . import views
app_name="Posts"
urlpatterns = [
   path('create/',views.PostCreateView.as_view(),name="createpost"),
   path('edit/',views.PostEditView.as_view(),name="editpost"),
   path('delete/<int:post_id>/<slug:user_id>/',views.PostDeleteView.as_view(),name="postdelete"),
   path('user/retrieve/',views.PostUserRetriveView.as_view(),name="postuser"),
   path('user/city/retrieve/',views.PostUserCityRetriveView.as_view(),name="postusercity"),
   path('saved/<int:post_id>/<slug:user_id>/',views.PostSavedView.as_view(),name="postsaved"),
]
