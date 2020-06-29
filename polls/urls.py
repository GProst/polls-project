from django.urls import include
from rest_framework.routers import DefaultRouter
from polls import views
from django.urls import path

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'polls', views.PollsViewSet)
router.register(r'questions', views.QuestionsViewSet)

urlpatterns = [
  path('', include(router.urls)),
]
