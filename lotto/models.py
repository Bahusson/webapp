from django.db import models

class Lotto(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    readme = models.TextField()
    image = models.ImageField(upload_to='images')
    version = models.CharField(max_length=25)
    weight = models.CharField(max_length=25)
    compatible = models.CharField(max_length=200)
    downlink = models.TextField()
    gitsrccode = models.TextField(blank=True)
    license = models.CharField(max_length=250, blank=True)

    #Ta funkcja pokazuje tytuł postu na stronie admina. Zawsze używaj ___str___ żeby wrzucić coś w górę do adminów.
    def __str__(self):
        return self.title

    #Funkcja formatująca datę w ludzki sposób...
    def date_short(self):
        return self.date.strftime('%a %d %b %Y')

    def summary(self):
        return self.readme[:110]
# Create your models here.
