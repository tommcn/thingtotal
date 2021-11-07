from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import EntryViewset, StreamViewset

router = DefaultRouter()
router.register(r"stream", StreamViewset, basename="stream")

entries_router = routers.NestedDefaultRouter(
    router,
    r"stream",
    lookup="stream"
)
entries_router.register(
    r"entries",
    EntryViewset,
    basename="stream-entries"
)

urlpatterns = router.urls
urlpatterns += entries_router.urls
