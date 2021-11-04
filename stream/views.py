from rest_framework import mixins, viewsets
import bson
from stream.models import Stream
from rest_framework.response import Response
from stream.serializers import StreamSerializer
# Create your views here.


class StreamViewset(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

    def get_object(self):
        queryset = self.get_queryset()
        # Remember to convert the `pk` argument from `str` to `ObjectId`
        # since Mongo expects it to be that way.
        obj = queryset.filter(pk=bson.ObjectId(self.kwargs['pk'])).first()
        return obj
