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
class Game1(models.Model):
    Id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    N1 = models.IntegerField()
    N2 = models.IntegerField()
    N3 = models.IntegerField()
    N4 = models.IntegerField()
    N5 = models.IntegerField()
    N6 = models.IntegerField()
    N7 = models.IntegerField()
    N8 = models.IntegerField()
    N9 = models.IntegerField()
    N10 = models.IntegerField()
    N11 = models.IntegerField()
    N12 = models.IntegerField()
    N13 = models.IntegerField()
    N14 = models.IntegerField()
    N15 = models.IntegerField()
    N16 = models.IntegerField()
    N17 = models.IntegerField()
    N18 = models.IntegerField()
    N19 = models.IntegerField()
    N20 = models.IntegerField()

    def __str__(self):
        return self.title

class Game2(models.Model):
    Id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    N1 = models.IntegerField()
    N2 = models.IntegerField()
    N3 = models.IntegerField()
    N4 = models.IntegerField()
    N5 = models.IntegerField()
    N6 = models.IntegerField()

    def __str__(self):
        return self.title

class Game3(models.Model):
    Id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    N1 = models.IntegerField()
    N2 = models.IntegerField()
    N3 = models.IntegerField()
    N4 = models.IntegerField()
    N5 = models.IntegerField()

    def __str__(self):
        return self.title

class Game4(models.Model):
    Id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    N1 = models.IntegerField()
    N2 = models.IntegerField()
    N3 = models.IntegerField()
    N4 = models.IntegerField()
    N5 = models.IntegerField()
    R1 = models.IntegerField()

    def __str__(self):
        return self.title
