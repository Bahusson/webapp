from modeltranslation.translator import translator, TranslationOptions
from myprograms.models import ProgramPage, MyProgram, RandomizerItems


class ProgramPageTranslate(TranslationOptions):
    fields = (
     'big_intro', 'small_intro', 'send_email', 'published', 'version',
     'system', 'weight', 'license', 'download_exe', 'link_git', 'details',
     'launch_new',)


translator.register(ProgramPage, ProgramPageTranslate)


class MyProgramTranslate(TranslationOptions):
    fields = ('title', 'readme', 'image', 'compatible', 'license',)


translator.register(MyProgram, MyProgramTranslate)


class RandomizerItemsTranslate(TranslationOptions):
    fields = (
     'title', 'sel1', 'sel2', 'sel3', 'sel4', 'mark_selection', 'start_date',
     'mark_all', 'end_date', 'gen_stats', 'hi_low', 'no_raw', 'mode', 'count',
     'avg', 'gen', 'chart', 'score', 'save_sc', 'saveme', 'your', 'play',
     'nums',)


translator.register(RandomizerItems, RandomizerItemsTranslate)
