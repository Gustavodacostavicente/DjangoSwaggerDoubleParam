from django.urls import path, re_path
#from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from .apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate

schema_view = get_schema_view(
   openapi.Info(
      title="Django Data Provider API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# router = DefaultRouter()
# router.register('polls', PollViewSet, basename='polls')


urlpatterns = [
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


# urlpatterns += router.urls