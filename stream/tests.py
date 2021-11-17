"""
lmao copilot wrote all of the test cases from function names
"""
import json

import bson
from django.test import Client, TestCase

from .models import Entry, Stream


# Create your tests here.
class TestStream(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_stream(self):
        with open("stream/schema/example.json") as f:
            schema = json.load(f)

        res = self.client.post(
            "/api/stream/",
            {
                "name": "test_stream",
                "description": "test stream",
                "fields": json.dumps(schema),  # Don't know why dumps is needed
            },
        )
        s = Stream.objects.all()

        self.assertEquals(res.status_code, 201)

        self.assertEquals(s.count(), 1)
        self.assertEquals(s.first().name, "test_stream")
        self.assertEquals(s.first().description, "test stream")
        self.assertEquals(s.first().fields, schema)

    def test_create_stream_with_invalid_schema(self):
        res = self.client.post(
            "/api/stream/",
            {
                "name": "test_stream",
                "description": "test stream",
                "fields": "invalid json",
            },
        )

        self.assertEquals(res.status_code, 400)

    def test_create_stream_with_invalid_schema_type(self):
        res = self.client.post(
            "/api/stream/",
            {
                "name": "test_stream",
                "description": "test stream",
                "fields": [True],
            },
            content_type="application/json",
        )

        self.assertEquals(res.status_code, 400)

    def test_update_stream(self):
        with open("stream/schema/example.json") as f:
            schema = json.load(f)

        s = Stream.objects.create(
            name="test_stream", description="test stream", fields=schema
        )

        res = self.client.put(
            f"/api/stream/{s._id}/",
            {
                "name": "test_stream_updated",
                "description": "test stream updated",
                "fields": schema,  # Don't know why dumps is needed
            },
            content_type="application/json",
        )
        s = Stream.objects.all()

        self.assertEquals(res.status_code, 200)

        self.assertEquals(s.count(), 1)
        self.assertEquals(s.first().name, "test_stream_updated")
        self.assertEquals(s.first().description, "test stream updated")
        self.assertEquals(s.first().fields, schema)

    def test_update_stream_with_invalid_schema(self):
        s = Stream.objects.create(
            name="test_stream", description="test stream", fields={"a": "b"}
        )

        res = self.client.put(
            f"/api/stream/{s._id}/",
            {
                "name": "test_stream_updated",
                "description": "test stream updated",
                "fields": "invalid json",
            },
            content_type="application/json",
        )

        self.assertEquals(res.status_code, 400)

    def test_update_stream_with_invalid_schema_type(self):
        s = Stream.objects.create(
            name="test_stream", description="test stream", fields={"a": "b"}
        )

        res = self.client.put(
            f"/api/stream/{s._id}/",
            {
                "name": "test_stream_updated",
                "description": "test stream updated",
                "fields": [True],
            },
            content_type="application/json",
        )

        self.assertEquals(res.status_code, 400)

    def test_delete_stream(self):
        with open("stream/schema/example.json") as f:
            schema = json.load(f)

        s = Stream.objects.create(
            name="test_stream", description="test stream", fields=schema
        )

        res = self.client.delete(f"/api/stream/{s._id}/")

        self.assertEquals(res.status_code, 204)
        self.assertEquals(Stream.objects.all().count(), 0)

    def test_get_stream(self):
        with open("stream/schema/example.json") as f:
            schema = json.load(f)

        s = Stream.objects.create(
            name="test_stream", description="test stream", fields=schema
        )

        res = self.client.get(f"/api/stream/{s._id}/")

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            {
                "_id": str(s._id),
                "name": "test_stream",
                "description": "test stream",
                "fields": schema,
            },
        )

    def test_get_stream_with_invalid_id(self):
        res = self.client.get(f"/api/stream/{bson.ObjectId()}/")

        self.assertEquals(res.status_code, 404)

    def test_get_streams(self):
        with open("stream/schema/example.json") as f:
            schema = json.load(f)

        s = Stream.objects.create(
            name="test_stream", description="test stream", fields=schema
        )

        res = self.client.get("/api/stream/")

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            [
                {
                    "_id": str(s._id),
                    "name": "test_stream",
                    "description": "test stream",
                    "fields": schema,
                }
            ],
        )


class TestEntry(TestCase):
    def setUp(self):
        self.client = Client()
        with open("stream/schema/example.json") as f:
            schema = json.load(f)

        s = Stream.objects.create(
            name="test_stream", description="test stream", fields=schema
        )
        self.stream_id = s._id

    def test_create_entry(self):
        res = self.client.post(
            f"/api/stream/{self.stream_id}/entries/",
            {"data": {"time": 0, "temp": 0}},
            content_type="application/json",
        )

        self.assertEquals(res.status_code, 201)
        self.assertEquals(
            Entry.objects.filter(stream_id=self.stream_id).count(), 1
        )

    def test_create_entry_with_invalid_data(self):
        res = self.client.post(
            f"/api/stream/{self.stream_id}/entries/",
            {"data": "invalid json"},
            content_type="application/json",
        )

        self.assertEquals(res.status_code, 400)
        self.assertEquals(
            Entry.objects.filter(stream_id=self.stream_id).count(), 0
        )

    def test_create_entry_with_invalid_data_type(self):
        res = self.client.post(
            f"/api/stream/{self.stream_id}/entries/",
            {"data": [True]},
            content_type="application/json",
        )

        self.assertEquals(res.status_code, 400)
        self.assertEquals(
            Entry.objects.filter(stream_id=self.stream_id).count(), 0
        )

    def test_create_entry_with_invalid_stream_id(self):
        res = self.client.post(
            f"/api/stream/{bson.ObjectId()}/entries/",
            {"data": {"time": 0, "temp": 0}},
            content_type="application/json",
        )
        self.assertEquals(res.status_code, 404)
        self.assertEquals(Entry.objects.all().count(), 0)

    def test_get_entries_empty(self):
        res = self.client.get(f"/api/stream/{self.stream_id}/entries/")

        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.json(), [])

    def test_get_entries(self):
        with open("stream/schema/example.json") as f:
            schema = json.load(f)

        s = Stream.objects.create(
            name="test_stream", description="test stream", fields=schema
        )

        e1 = Entry.objects.create(stream_id=s._id, data={"time": 0, "temp": 0})
        e2 = Entry.objects.create(stream_id=s._id, data={"time": 1, "temp": 1})

        res = self.client.get(f"/api/stream/{s._id}/entries/")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            [
                {"_id": str(e1._id), "data": {"time": 0, "temp": 0}},
                {"_id": str(e2._id), "data": {"time": 1, "temp": 1}},
            ],
        )

    def test_get_entries_with_invalid_stream_id(self):
        res = self.client.get(f"/api/stream/{bson.ObjectId()}/entries/")

        self.assertEquals(res.status_code, 404)
        self.assertEquals(Entry.objects.all().count(), 0)
