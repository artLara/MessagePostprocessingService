from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from .views import *

# router = routers.DefaultRouter()
# router.register(r'classifier', views.Post_APIView, 'classifier')

urlpatterns = [
    path('api/v1/', Post_APIView.as_view()),
    path('docs', include_docs_urls(title='Message PostProcessing API'))
]
