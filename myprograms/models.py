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
    place = models.CharField(max_length=3)

    # Ta funkcja pokazuje tytuł postu na stronie admina.
    def __str__(self):
        return self.title

    # Funkcja formatująca datę w ludzki sposób...
    def date_short(self):
        return self.date.strftime('%a %d %b %Y')

    # Zwraca skrócony opis,
    def summary(self):
        return self.readme[:110]

    class Meta:
        ordering = ['-place']


# Specjalna klasa tylko dla tłumaczenia programu
class RandomizerItems(models.Model):
    title = models.CharField(max_length=100)  # Nazwa programu
    sel1 = models.CharField(max_length=100)  # Opcje 1-4
    sel2 = models.CharField(max_length=100)  # Typu radio
    sel3 = models.CharField(max_length=100)
    sel4 = models.CharField(max_length=100)
    mark_selection = models.CharField(max_length=100)  # Zaznacz pomiary
    start_date = models.CharField(max_length=100)  # Data początkowa
    mark_all = models.CharField(max_length=100)  # Całość pomiarów
    end_date = models.CharField(max_length=100)  # Data końcowa
    gen_stats = models.CharField(max_length=100)  # Generuj statystyki
    hi_low = models.CharField(max_length=100)  # Najczęstsza/najrzadsza liczba
    no_raw = models.CharField(max_length=100)  # Bez gołych losowań
    mode = models.CharField(max_length=100)  # Najczęstsze liczby
    count = models.CharField(max_length=100)  # Ile chcesz ww liczb
    avg = models.CharField(max_length=100)  # Średnie wyników losowań
    gen = models.CharField(max_length=100)  # Generuj
    chart = models.CharField(max_length=100)  # Generuj wykres
    score = models.CharField(max_length=100)  # Generuj raport
    save_sc = models.CharField(max_length=100)  # Zapisz raport
    saveme = models.CharField(max_length=100)  # Zapisz
    your = models.CharField(max_length=100)  # Twój raport
    play = models.CharField(max_length=100)  # Zagraj w wybraną grę
    nums = models.CharField(max_length=100)  # Twoje liczby
