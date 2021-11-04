from rest_framework.routers import DefaultRouter
from .views import StreamViewset


router = DefaultRouter()
router.register(r'stream', StreamViewset, basename='stream')
urlpatterns = router.urls
