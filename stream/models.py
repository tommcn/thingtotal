from djongo import models


# Create your models here.
class Stream(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    fields = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class Entry(models.Model):
    _id = models.ObjectIdField()
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
