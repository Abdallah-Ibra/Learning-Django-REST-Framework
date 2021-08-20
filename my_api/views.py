from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

### Function API View ###

@api_view(['GET','POST'])
def article_list(request):
   
   if request.method == 'GET':
      articles = Article.objects.all()
      serializer = ArticleSerializer(articles, many=True)
      return Response(serializer.data)
   
   elif request.method == 'POST':
      serializer = ArticleSerializer(data=request.data)
      
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def article_detail(request, pk):
   
   try:
      article = Article.objects.get(pk=pk)
   except Article.DoesNotExist:
      return HttpResponse(status=status.HTTP_404_NOT_FOUND)
   
   if request.method == 'GET':
      serializer = ArticleSerializer(article)
      return Response(serializer.data)
   
   elif request.method == 'PUT':
      serializer = ArticleSerializer(article, data=request.data)
      
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   elif request.method == 'DELETE':
      article.delete()
      return HttpResponse(status= status.HTTP_204_NO_CONTENT)
   


### Class Based API View ###

class ArticleAPIView(APIView):
   
   def get(self, request):
      article = Article.objects.all()
      serializer = ArticleSerializer(article, many= True)
      return Response(serializer.data)
   
   def post(self, request):
      serializer = ArticleSerializer(data= request.data)
      
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status= status.HTTP_201_CREATED)
      return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class ArticleAPIViewDetails(APIView):
   
   def get_object(self,id):
      try:
         return Article.objects.get(id=id)
      except Article.DoesNotExist:
         return HttpResponse(status= status.HTTP_404_NOT_FOUND)

   def get(self,request,id):
      article = self.get_object(id=id)
      serializer = ArticleSerializer(article)
      return Response(serializer.data)
   
   def put(self,request,id):
      article = self.get_object(id=id)
      serializer = ArticleSerializer(article, data=request.data)
      
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
   def delete(self, request,id):
      article = self.get_object(id)
      article.delete()
      return Response(status= status.HTTP_204_NO_CONTENT)


### Generic Views & Mixins ###

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
   serializer_class = ArticleSerializer
   queryset = Article.objects.all()
   lookup_field = 'id'
   # authentication_classes = [SessionAuthentication, BasicAuthentication]
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]
   
   def get(self, request,id):
      if id:
         return self.retrieve(request)
      else:
         return self.list(request)
         
   
   def post(self, request,id):
      return self.create(request,id)
   
   def put(self, request, id):
      return self.update(request, id)
   
   def delete(self, request, id):
      return self.destroy(request, id)
   
   
class GenericListAPIView(generics.ListCreateAPIView): ## Show Data And Can Add A new Job
   serializer_class = ArticleSerializer
   queryset = Article.objects.all()


### ViewSets ###

class ArticleViewSet(viewsets.ViewSet):
   
   def list(self, request):
      article = Article.objects.all()
      serializer = ArticleSerializer(article, many= True)
      return Response(serializer.data)
   
   def create(self,request):
      serializer = ArticleSerializer(data= request.data)
      
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status= status.HTTP_201_CREATED)
      return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

   def retrieve(self, request, pk=None):
      queryset = Article.objects.all()
      article = get_object_or_404(queryset, pk=pk)
      serializer = ArticleSerializer(article)
      return Response(serializer.data)
   
   def update(self, request, pk=None):
      queryset = Article.objects.all()
      article = get_object_or_404(queryset, pk=pk)
      serializer = ArticleSerializer(article, data= request.data)
   
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
   def destroy(self, request, pk=None):
      queryset = Article.objects.all()
      article = get_object_or_404(queryset, pk=pk)
      article.delete()
      return Response(status= status.HTTP_204_NO_CONTENT)