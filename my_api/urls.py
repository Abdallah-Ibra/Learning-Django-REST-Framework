from django.urls import path, include

from . import views

urlpatterns = [
   
   ### Function API View ###
   path('api/v1/article/', views.article_list),
   path('api/v1/article/<int:pk>', views.article_detail),
   
   ### Class Based API View ###
   path('api/v2/article/', views.ArticleAPIView.as_view()),
   path('api/v2/article/<int:id>', views.ArticleAPIViewDetails.as_view()),
   
   ### Generic Views & Mixins ###
   path('api/v3/article/', views.GenericListAPIView.as_view()),
   path('api/v3/article/<int:id>', views.GenericAPIView.as_view()),

   ]
