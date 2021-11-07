import bson
from rest_framework import viewsets

from stream.models import Entry, Stream
from stream.serializers import EntrySerializer, StreamSerializer


# Create your views here.
class StreamViewset(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

    def get_object(self):
        queryset = self.get_queryset()
        # Remember to convert the `pk` argument from `str` to `ObjectId`
        # since Mongo expects it to be that way.
        obj = queryset.filter(pk=bson.ObjectId(self.kwargs["pk"])).first()
        return obj


class EntryViewset(viewsets.ModelViewSet):
    queryset = Entry.objects.none()
    serializer_class = EntrySerializer

    def get_queryset(self):
        s = Stream.objects.get(pk=bson.ObjectId(self.kwargs["stream_pk"]))
        objs = Entry.objects.filter(stream=s)
        return objs

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(pk=bson.ObjectId(self.kwargs["pk"])).first()
        return obj