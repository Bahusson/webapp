from django.db import models


class Pageitem(models.Model):
    lang_flag = models.ImageField(upload_to='images')  # Mały obrazek języka
    headtitle = models.CharField(max_length=200)  # Nagłówek strony
    mainpage = models.CharField(max_length=200)  # Strona główna w tym języku
    news = models.CharField(max_length=200)  # Aktualności
    blog = models.CharField(max_length=200)  # Blog w tym języku
    download = models.CharField(max_length=200)  # programy w tym języku
    contact = models.CharField(max_length=200)  # Kontakt w tym języku
    send_email = models.CharField(max_length=200)  # Ważne pliki
    login = models.CharField(max_length=200)  # Zaloguj
    logout = models.CharField(max_length=200)  # Wyloguj
    see_cert = models.CharField(max_length=200)  # Pobierz Certyfikat
    skills_all = models.CharField(max_length=200)  # Wszystkie Umiejętności
    download_cv = models.CharField(max_length=200)  # Ściągnij moje CV
    download_pdf = models.CharField(max_length=200)  # Ściągnij jako PDF
    blogfeed = models.CharField(max_length=200)  # Wpisy na blogu poz.2
    carryon = models.CharField(max_length=200)  # Czytaj dalej...
    newcode = models.CharField(max_length=200)  # Najnowszy program.
    worthwhile = models.CharField(max_length=200)  # Warte przeczytania
    about = models.CharField(max_length=200)  # O stronie
    pageinfo = models.CharField(max_length=300)  # Cośtam o stronie
    myskills = models.CharField(max_length=200)  # Moje umiejętności
    welcome = models.CharField(max_length=200)  # Przywitanie na głównej
    intro = models.CharField(max_length=300)  # Intro na głównej
    other = models.CharField(max_length=200)  # Inne strony
    github = models.CharField(max_length=200)  # tekst linku do githuba
    git_link = models.CharField(max_length=200)  # link do githuba
    gitter = models.CharField(max_length=200)  # tekst linku do gittera
    gitter_link = models.CharField(max_length=200)  # link do gittera


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


class Curriculum(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='assets', blank=True, null=True)

    def __str__(self):
        return self.title
