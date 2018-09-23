from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images')
    summary = models.TextField()
    link = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    def shortsum(self):
        return self.summary[:200]

class Tech(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    body = models.TextField()
    link = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    def linkifblank(self):
        if self.link == None:
            return 0
        else:
            return self
