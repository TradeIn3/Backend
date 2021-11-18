from django.contrib import admin
from django.urls import path,include
from . import views
app_name="Posts"
urlpatterns = [
   path('create/',views.PostCreateView.as_view(),name="createpost"),
   path('edit/',views.PostEditView.as_view(),name="editpost"),
   path('delete/',views.PostDeleteView.as_view(),name="postdelete"),
   path('user/retrieve/',views.PostUserRetriveView.as_view(),name="postuser"),
   path('all/retrieve/',views.PostRetriveView.as_view(),name="allpost"),
   path('single/retrieve/',views.SinglePostRetriveView.as_view(),name="singlepost"),
   path('save/',views.PostSavedView.as_view(),name="postsaved"),
   path('question/',views.PostQuestionView.as_view(),name="postaskquestion"),
   path('answer/',views.PostAnswerView.as_view(),name="postanswer"),
   path('productpay/', views.StartProductPayment.as_view(), name="payment"),
   path('productpayment/success/', views.HandleProductPaymentSuccess.as_view(), name="payment_success"),
   path('reservepay/', views.StartReservedPayment.as_view(), name="payment"),
   path('reservepayment/success/', views.HandleReservedPaymentSuccess.as_view(), name="payment_success"),
   path('allbrands/',views.AllBrands.as_view(),name="all_brands")
]
