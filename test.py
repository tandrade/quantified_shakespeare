import pickle
from common.play_data import plays
from common.models import Play, DataAssembler, FacetedLineChart
from projects.chars_on_stage import CharsOnStage
from projects.bechdel_test import BechdelTest
from projects.play_analyzer import WordAnalyzer

# charsData = DataAssembler(["action_i", "scene_i", "action_type", "total_words", "total_characters"])
# for play, play_data in plays.iteritems():
#     p = Play('data/%s' % play, play_data['full_name'], play_data['genre'])
#     b = BechdelTest(p)
#     b.analyze()

p = Play('data/1H4.xml', 'HenryIV Part I', 'history')
b = BechdelTest(p)
b.analyze()