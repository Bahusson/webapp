from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images')
    summary = models.TextField()

    def __str__(self):
        return self.title

    def shortsum(self):
        return self.summary[:200]
