import os

from common.play_data import plays
from common.models import Play, DataAssembler, FacetedLineChart
from projects.chars_on_stage import CharsOnStage, BechdelTest
from projects.play_analyzer import WordAnalyzer

# TODO: test how well DataAssembler works for WordAnalyzer
# TODO: refactor to make this a command line call
# for testing purposes
i = 0
charsData = DataAssembler(["action_i", "scene_i", "action_type", "total_words", "total_characters"])
for play, play_data in plays.iteritems():
    if i > 0:
        break
    p = Play('data/%s' % play, play_data['full_name'], play_data['genre'])
    b = BechdelTest(p)

