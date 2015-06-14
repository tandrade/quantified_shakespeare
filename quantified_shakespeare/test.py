import os

from common.play_data import plays
from common.models import Play, DataAssembler
from projects.chars_on_stage import CharsOnStage
from projects.play_analyzer import WordAnalyzer

# TODO: just pass the play label, not the play object
# TODO: test how well DataAssembler works for WordAnalyzer
charsData = DataAssembler(["action_i", "scene_i", "action_type", "total_words", "total_characters"])
i = 0
for play in plays:
    p = Play(os.path.join(os.path.expanduser('~'), 'Documents', 'shakespeare', play))
    c = CharsOnStage(p)
    # w = WordAnalyzer(p)
    charsData.add_data_to_parse(c.data, p)
    i += 1

charsData.create_matrix()

# also for testing
# print charsData.matrix.head()

