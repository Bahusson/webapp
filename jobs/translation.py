from modeltranslation.translator import translator, TranslationOptions
from jobs.models import Job
from jobs.models import Tech


class JobTranslate(TranslationOptions):
    fields = ('title', 'summary',)


translator.register(Job, JobTranslate)


class TechTranslate(TranslationOptions):
    fields = ('title', 'body',)


translator.register(Tech, TechTranslate)
