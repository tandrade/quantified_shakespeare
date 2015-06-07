import os

from common.models import Play, Display
from projects.chars_on_stage import CharsOnStage

TEST_PLAY = os.path.join(os.path.expanduser('~'), 'Documents', 'shakespeare', '1H4.xml')
TEST_PLAY_2 = os.path.join(os.path.expanduser('~'), 'Documents', 'shakespeare', '2H4.xml')

c = CharsOnStage(Play(TEST_PLAY))
d = Display("num_words", "chars_on_stage", y_max=20, x_max=35000,
            y_display="Characters on stage", x_display="Play time (in words)")
d.add_data(c.data, TEST_PLAY)
c = CharsOnStage(Play(TEST_PLAY_2))
d.add_data(c.data, TEST_PLAY_2)
d.display()