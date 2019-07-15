from modeltranslation.translator import translator, TranslationOptions
from blog.models import Blog


class BlogTranslate(TranslationOptions):
    fields = ('title', 'body',)


translator.register(Blog, BlogTranslate)
