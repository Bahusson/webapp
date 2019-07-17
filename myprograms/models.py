from django.db import models


# Klasa wspólna dla tłumaczeń części o programach.
class ProgramPage(models.Model):
    big_intro = models.CharField(max_length=50)
    small_intro = models.CharField(max_length=300)
    send_email = models.CharField(max_length=30)
    published = models.CharField(max_length=30)
    version = models.CharField(max_length=20)
    system = models.CharField(max_length=20)
    weight = models.CharField(max_length=25)
    license = models.CharField(max_length=25)
    download_exe = models.CharField(max_length=200)
    link_git = models.CharField(max_length=200)
    details = models.CharField(max_length=25)
    launch_new = models.CharField(max_length=40)


# Klasa dla poszczególnych programów.
class MyProgram(models.Model):
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
    linkinside = models.CharField(max_length=250, blank=True)

    # Ta funkcja pokazuje tytuł postu na stronie admina.
    def __str__(self):
        return self.title

    # Funkcja formatująca datę w ludzki sposób...
    def date_short(self):
        return self.date.strftime('%a %d %b %Y')

    # Zwraca skrócony opis,
    def summary(self):
        return self.readme[:110]

#class RandomizerItems(models.Model):
#    title =
