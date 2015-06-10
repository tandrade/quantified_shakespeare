import os

from common.play_data import plays
from common.models import Play, Display
from projects.chars_on_stage import CharsOnStage
from projects.play_analyzer import WordAnalyzer

# d = Display("num_words", "chars_on_stage", y_max=20, x_max=35000,
#             y_display="Characters on stage", x_display="Play time (in words)")
#
for play in plays:
    p = Play(os.path.join(os.path.expanduser('~'), 'Documents', 'shakespeare', play))
    c = CharsOnStage(p)
    w = WordAnalyzer(p)