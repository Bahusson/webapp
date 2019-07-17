from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)
    pubdate = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='images')
    video = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:110]

    def pubdate_short(self):
        return self.pubdate.strftime('%a %d %b %Y')
