from django.contrib import admin
from django.urls import path,include
from . import views
app_name="Posts"
urlpatterns = [
   path('create/',views.PostCreateView.as_view(),name="createpost"),
   path('edit/<int:post_id>/',views.PostEditView.as_view(),name="editpost"),
   path('delete/',views.PostDeleteView.as_view(),name="postdelete"),
   path('user/retrieve/',views.PostUserRetriveView.as_view(),name="postuser"),
   path('user/city/retrieve/',views.PostRetriveView.as_view(),name="postusercity"),
   path('saved/',views.PostSavedView.as_view(),name="postsaved"),
   path('question/',views.PostQuestionView.as_view(),name="postaskquestion"),
]
