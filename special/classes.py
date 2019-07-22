class PageLoad(object):
    ''' Zwraca tyle języków ile mamy zainstalowane
    w ustawieniach w zakładce LANGUAGES w formacie naprzemiennym
    pasującym do wzornika z dwoma wyjściowymi
    (ID_Języka, Ścieżka_Flagi_Języka), oraz
    Ładuje wszystkie podstawowe elementy w widoku strony. '''

    def __init__(self, *args):
        lang_id = []
        langsl = []
        a = args[0]
        b = args[1]
        self.langs = []
        locations = list(a.objects.all())
        self.items = locations[0]
        for item in b:
            lang_id.append("lang_flag_" + str(item[0]))

        x = len(lang_id)-1
        y = 0

        while x+1 > 0:
            z = self.items.__dict__[lang_id[y]]
            langsl.append(z)
            x = x-1
            y = y+1

        self.langs = zip(lang_id, langsl)


class Blog(PageLoad):
    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(*args)

    def gen(self, **kwargs):
        b = kwargs['B']
        self.bloglist = list(b.objects.all())
        self.blogs = b.objects

        if 'blogid' in kwargs:
            G404 = kwargs['G404']
            blog_id = kwargs['blogid']
            self.blog = G404(b, pk=blog_id)


class Trick(PageLoad):
    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(*args)

    def gen(self, **kwargs):
        tr = kwargs['Tr']
        self.tricks = tr.objects

        if 'tricksid' in kwargs:
            G404 = kwargs['G404']
            tricks_id = kwargs['tricksid']
            self.trick = G404(tr, pk=tricks_id)


class Tech(PageLoad):
    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(*args)

    def gen(self, **kwargs):
        te = kwargs['Te']
        self.techs = te.objects

        if 'techsid' in kwargs:
            G404 = kwargs['G404']
            techs_id = kwargs['techsid']
            self.tech = G404(te, pk=techs_id)


class CV(object):
    def __init__(self, **kwargs):
        cvs = kwargs['Cv']
        cvlist = list(cvs.objects.all())
        self.cv = cvlist[0]


class Showroom(PageLoad):
    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(*args)

    def gen(self, **kwargs):
        pp = kwargs['Pp']
        mp = kwargs['Mp']
        firstp = list(pp.objects.all())
        self.proglist = list(mp.objects.all())
        self.pritems = firstp[0]
        self.myprogs = mp.objects

        if 'place' in kwargs:
            G404 = kwargs['G404']
            place_pr = kwargs['place']
            self.myprog = G404(mp, pk=place_pr)

    def randomizer(self, **kwargs):
        randob = kwargs['Randomizer']
        randlist = list(randob.objects.all())
        self.randitem = randlist[0]
