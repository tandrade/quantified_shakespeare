import os

from common.play_data import plays
from common.models import Play, DataAssembler
from projects.chars_on_stage import CharsOnStage
from projects.play_analyzer import WordAnalyzer

# TODO: test how well DataAssembler works for WordAnalyzer
# TODO: define relative path of the play data
# TODO: refactor to make this a command line call
charsData = DataAssembler(["action_i", "scene_i", "action_type", "total_words", "total_characters"])
for play, play_data in plays.iteritems():
    p = Play(os.path.join(os.path.expanduser('~'), 'Documents', 'shakespeare', play),
             play_data['full_name'], play_data['genre'])
    c = CharsOnStage(p)
    # w = WordAnalyzer(p)
    charsData.add_data_to_parse(c.data, p.title)

charsData.create_matrix()

# also for testing
print charsData.matrix.head()

