import bson
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
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
        obj = get_object_or_404(queryset, pk=bson.ObjectId(self.kwargs["pk"]))
        return obj


class EntryViewset(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def get_queryset(self):
        try:
            s = Stream.objects.get(pk=bson.ObjectId(self.kwargs["stream_pk"]))
        except Stream.DoesNotExist:
            raise Http404("Stream does not exist")
        objs = Entry.objects.filter(stream=s)
        return objs

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=bson.ObjectId(self.kwargs["pk"]))
        return obj
