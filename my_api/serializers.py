from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.Serializer):
   class Meta:
      model = Article
      fields = ['id','title','author']