from django.db import models


class Pageitem(models.Model):
    lang_flag = models.ImageField(upload_to='images')  # Mały obrazek języka
    headtitle = models.CharField(max_length=200)  # Nagłówek strony w tym języku
    mainpage = models.CharField(max_length=200)  # Strona główna w tym języku
    news = models.CharField(max_length=200)  # Aktualności
    blog = models.CharField(max_length=200)  # Blog w tym języku
    download = models.CharField(max_length=200)  # pobieranie akademików w tym języku
    contact = models.CharField(max_length=200)  # Kontakt w tym języku
    send_email = models.CharField(max_length=200)  # Ważne pliki
    login = models.CharField(max_length=200, blank=True, null=True)  # Zaloguj
    logout = models.CharField(max_length=200)  # Wyloguj


class Trick(models.Model):
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
    image = models.ImageField(upload_to='images', blank=True)
    body = models.TextField()
    file = models.FileField(upload_to='assets', blank=True, null=True)

    def __str__(self):
        return self.title

    def linkifblank(self):
        if self.file is None:
            return 0
        else:
            return self
