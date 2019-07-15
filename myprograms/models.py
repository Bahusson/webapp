from django.db import models


# Klasa wspólna dla tłumaczeń części o programach.
class ProgramPage(models.Model):
    big_intro = models.Charfield(max_length=50)
    small_intro = models.Charfield(max_length=300)
    send_email = models.charfield(max_length=30)
    published = models.CharField(max_length=30)
    version = models.Charfield(max_length=20)
    system = models.Charfield(max_length=20)
    weight = models.CharField(max_length=25)
    license = models.CharField(max_length=25)
    download_exe = models.Charfield(max_length=200)
    link_git = models.Charfield(max_length=200)
    details = models.CharField(max_length=25)
    launch_new = models.Charfield(max_lenght=40)


# Klasa dla poszczególnych programów. Można by zmienić nazwę. Tak jakoś dziwnie zostało...
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

    # Ta funkcja pokazuje tytuł postu na stronie admina. Zawsze używaj ___str___ żeby wrzucić coś w górę do adminów.
    def __str__(self):
        return self.title

    # Funkcja formatująca datę w ludzki sposób...
    def date_short(self):
        return self.date.strftime('%a %d %b %Y')

    # Zwraca skrócony opis, gdyby kiedyś był gdzieś potrzebny. Np. w zestawieniu programów.
    def summary(self):
        return self.readme[:110]
# Create your models here.
