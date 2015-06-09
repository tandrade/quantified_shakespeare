import os

from common.play_data import plays
from common.models import Play, Display
from projects.chars_on_stage import CharsOnStage

d = Display("num_words", "chars_on_stage", y_max=20, x_max=35000,
            y_display="Characters on stage", x_display="Play time (in words)")

# display works best if there's about 5 plots
# TODO: add colors
max_disp = 4
i = 0
for p in plays:
    if i > max_disp:
        break
    c = CharsOnStage(Play(os.path.join(os.path.expanduser('~'), 'Documents', 'shakespeare', p)))
    d.add_data(c.data, p, plays[p]['full_name'])
    i += 1

d.display()