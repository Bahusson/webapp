from modeltranslation.translator import translator, TranslationOptions
from jobs.models import Pageitem, Trick, Tech


class PageitemTranslate(TranslationOptions):
    fields = ('lang_flag', 'headtitle', 'mainpage', 'news', 'blog', 'download', 'contact', 'send_email', 'login', 'logout',)


translator.register(Pageitem, PageitemTranslate)


class TrickTranslate(TranslationOptions):
    fields = ('title', 'summary',)


translator.register(Trick, TrickTranslate)


class TechTranslate(TranslationOptions):
    fields = ('title', 'body',)


translator.register(Tech, TechTranslate)
