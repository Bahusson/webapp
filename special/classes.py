class PageLoad(object):
    ''' Zwraca tyle języków ile mamy zainstalowane
    w ustawieniach w zakładce LANGUAGES w formacie naprzemiennym
    pasującym do wzornika z dwoma wyjściowymi
    (ID_Języka, Ścieżka_Flagi_Języka), oraz
    Ładuje wszystkie podstawowe elementy w widoku strony. '''

    def __init__(self, a, b, *args, **kwargs):
        lang_id = []
        langsl = []
        self.langs = []
        locations = list(a.objects.all())
        self.items = locations[0]
        for item in b :
            lang_id.append("lang_flag_" + str(item[0]))

        x = len(lang_id) -1
        y = 0

        while x+1 > 0 :
            z = self.items.__dict__[lang_id[y]]
            langsl.append(z)
            x = x-1
            y = y+1

        self.langs = zip(lang_id, langsl)

    def portal(self, *args, **kwargs):
        f = args[0]
        i = args[1]
        b = args[2]
        G404 = args[3]
        self.files = f.objects
        self.infos = i.objects
        self.blogs = b.objects

        if 'blogid' in kwargs:
            blog_id = kwargs['blogid']
            self.blog = G404(b, pk=blog_id)

        if 'infoid' in kwargs:
            info_id = kwargs['infoid']
            self.info = G404(i, pk=info_id)
