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

    def portal(self, **kwargs):
        if 'B' in kwargs:
            b = kwargs['B']
            self.blogs = b.objects

        if 'Tr' in kwargs:
            tr = kwargs['Tr']
            self.tricks = tr.objects

        if 'Te' in kwargs:
            te = kwargs['Te']
            self.techs = te.objects

        if 'G404' in kwargs:
            G404 = kwargs['G404']

        if 'blogid' in kwargs:
            blog_id = kwargs['blogid']
            self.blog = G404(b, pk=blog_id)

        if 'tricksid' in kwargs:
            tricks_id = kwargs['tricksid']
            self.trick = G404(tr, pk=tricks_id)

        if 'techsid' in kwargs:
            techs_id = kwargs['techsid']
            self.techs = G404(te, pk=techs_id)

    def showroom(self, *args, **kwargs):
        if len(args) > 0:
            m = args[0]
            pp = args[1]
            self.myprogs = m.objects
            self.pritems = pp.objects

        if 'myprogramid' in kwargs:
            G404 = kwargs['G404']
            myprogram_id = kwargs['myprogramid']
            self.myprog = G404(m, pk=myprogram_id)
