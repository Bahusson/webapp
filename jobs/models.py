from django.db import models


class Pageitem(models.Model):
    lang_flag = models.ImageField(upload_to='images')  # Mały obrazek języka
    headtitle = models.CharField(max_length=200)  # Nagłówek strony
    mainpage = models.CharField(max_length=200)  # Strona główna w tym języku
    news = models.CharField(max_length=200)  # Aktualności
    blog = models.CharField(max_length=200)  # Blog w tym języku
    download = models.CharField(max_length=200)  # programy w tym języku
    contact = models.CharField(max_length=200)  # Kontakt / O mnie
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
    fresh_entries = models.CharField(max_length=200)  # Najnowsze wpisy.
    myphoto = models.ImageField(upload_to='images')  # Obrazek intro
    authphoto = models.ImageField(upload_to='images')  # Obrazek o mnie
    about_me = models.TextField()  # O mnie
    login_to_see = models.CharField(max_length=200)  # zaloguj by obejrzeć
    register = models.CharField(max_length=200)  # zarejestruj
    username = models.CharField(max_length=200)  # nazwa użytkownika
    password = models.CharField(max_length=200)  # hasło
    re_password = models.CharField(max_length=200)  # powt. hasło
    email = models.CharField(max_length=200)  # email


class Trick(models.Model):
    title = models.CharField(max_length=200, blank=True)
    pubdate = models.DateTimeField()
    image = models.ImageField(upload_to='images')
    summary = models.TextField()
    link = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-pubdate']

    def __str__(self):
        return self.title

    def shortsum(self):
        return self.summary[:200]


class Tech(models.Model):
    title = models.CharField(max_length=200)
    pubdate = models.DateTimeField()
    image = models.ImageField(upload_to='images')
    body = models.TextField()
    file = models.FileField(upload_to='assets', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pubdate']


class Curriculum(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='assets', blank=True, null=True)

    def __str__(self):
        return self.title
