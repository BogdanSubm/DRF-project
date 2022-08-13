from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('client/', views.ClientApiViewCreate.as_view(), name='client_create'),
    path('client/<int:client_id>/', views.ClientApiViewUpdate.as_view(), name='client_update'),
    path('mailing/', views.MailingApiViewCreate.as_view(), name='mailing_create'),
    path('mailing/<int:mailing_id>/', views.MailingApiViewUpdate.as_view(), name='mailing_update'),
]