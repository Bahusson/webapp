from modeltranslation.translator import translator, TranslationOptions
from lotto.models import MyProgram
from lotto.models import Lotto


class MyProgramTranslate(TranslationOptions):
    fields = ('bit_intro', 'small_intro', 'send_email', 'published', 'version', 'system', 'weight', 'license', 'download_exe', 'link_git', 'details', 'launch_new',)


translator.register(MyProgram, MyProgramTranslate)


class LottoTranslate(TranslationOptions):
    fields = ('title', 'readme', 'image', 'compatible', 'license',)


translator.register(Lotto, LottoTranslate)
