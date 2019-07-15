from modeltranslation.translator import translator, TranslationOptions
from jobs.models import Trick
from jobs.models import Tech


class TrickTranslate(TranslationOptions):
    fields = ('title', 'summary',)


translator.register(Trick, TrickTranslate)


class TechTranslate(TranslationOptions):
    fields = ('title', 'body',)


translator.register(Tech, TechTranslate)
