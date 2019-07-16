from modeltranslation.translator import translator, TranslationOptions
from jobs.models import Pageitem, Trick, Tech, Curriculum


class PageitemTranslate(TranslationOptions):
    fields = (
     'lang_flag', 'headtitle', 'mainpage', 'news', 'blog', 'download',
     'contact', 'send_email', 'login', 'logout', 'see_cert', 'skills_all',
     'download_cv', 'download_pdf', 'blogfeed', 'carryon', 'newcode',
     'worthwhile', 'about', 'pageinfo', 'myskills', 'welcome', 'intro',
     'other', 'github', 'gitter',)


translator.register(Pageitem, PageitemTranslate)


class TrickTranslate(TranslationOptions):
    fields = ('title', 'summary',)


translator.register(Trick, TrickTranslate)


class TechTranslate(TranslationOptions):
    fields = ('title', 'body',)


translator.register(Tech, TechTranslate)


class CurriculumTranslate(TranslationOptions):
    fields = ('title', 'file',)


translator.register(Curriculum, CurriculumTranslate)
