from modeltranslation.translator import translator, TranslationOptions
from myprograms.models import ProgramPage
from myprograms.models import MyProgram


class ProgramPageTranslate(TranslationOptions):
    fields = (
     'big_intro', 'small_intro', 'send_email', 'published', 'version',
     'system', 'weight', 'license', 'download_exe', 'link_git', 'details',
     'launch_new',)


translator.register(ProgramPage, ProgramPageTranslate)


class MyProgramTranslate(TranslationOptions):
    fields = ('title', 'readme', 'image', 'compatible', 'license',)


translator.register(MyProgram, MyProgramTranslate)
