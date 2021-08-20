from django.urls import path, include

from . import views

urlpatterns = [

   path('article/', views.article_list),
   path('article/<int:pk>', views.article_detail),
   ]
