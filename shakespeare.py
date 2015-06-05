import xml.dom.minidom as minidom
import pandas as pd
import matplotlib.pyplot as mpl
from ggplot import *

def clean_up_text(str):
  return str.strip()

class Play:
  def __init__(self, xml_file):
    self.data = minidom.parse(xml_file)    

class CharsOnStage():
  def __init__(self, play):
    self.play = play.data
    self._chars_on_stage = set() # who is on stage at any time 
    self._total_words = 0
    self.data = [] # results of calculation stored here
    self.calculate()

  def _handle_stage_events(self, e):
    e_type = e.getAttribute("type")
    update_value = 0
    chars = [char for char in e.getAttribute("who").split("#") if char != "" and not char.isupper()]
    if e_type == "entrance":
      for char in chars:
        if clean_up_text(char) not in self._chars_on_stage:
          self._chars_on_stage.add(clean_up_text(char))
          update_value += 1
    if e_type == "exit":
      for char in chars:
        if clean_up_text(char) in self._chars_on_stage:
          self._chars_on_stage.remove(clean_up_text(char))
          update_value -= 1
    return update_value

  def _handle_speech(self, e):
    char = e.getAttribute("who")[1:] # remove hashtag
    update_value = 0
    if char and char != "" and not char.isupper():
      if clean_up_text(char) not in self._chars_on_stage:
        self._chars_on_stage.add(clean_up_text(char))
        update_value += 1
    if len(e.getElementsByTagName("ab")) > 0:
      wds = len(e.getElementsByTagName("ab")[0].getElementsByTagName("w"))
      self._total_words += wds
    return update_value

  def calculate(self):
    acts = self.play.getElementsByTagName("div2")
    totals = []
    for act in acts:
      self._chars_on_stage = set() # reset who is on stage every act
      total_chars = 0
      actions = act.childNodes
      for action in actions:
        update = 0
        if action.nodeValue != "\n" and action.nodeValue != " \n":
          try: 
            if action.tagName == "stage":
              update = self._handle_stage_events(action)
            if action.tagName == "sp":
              update = self._handle_speech(action)
          except AttributeError:
            print action.nodeValue # should not be called: log the issue
        if update != 0:
          total_chars += update
          if total_chars != 0:
            self.data.append([self._total_words, total_chars])


class Display():

  title_column_name = "title"

  def __init__(self, x_label, y_label):
    self.y_label = y_label
    self.x_label = x_label
    self.agg_data = []

  # note: assumes two variables - x as first, y as second
  def add_data(self, data, label):
    self.agg_data += [[d[0], d[1], label] for d in data]

  def display(self, max_x=None, max_y=None):
    df = pd.DataFrame(self.agg_data, columns=[self.x_label, self.y_label, self.title_column_name])
    print ggplot(df, aes(x = self.x_label, y=self.y_label)) + geom_point()
    #TODO: call ggplot, facet on the title column
    #FIXME: ggplot's bar plot is broken because of changes to pandas API


all_plays = [
"1H4.xml",
# "2H4.xml",
# "2H6.xml",
# "3H6.xml",
# "Ado.xml",
# "Ant.xml",
# "AWW.xml",
# "AYL.xml",
# "Cor.xml",
# "Cym.xml",
# "Err.xml",
# "H5.xml",
# "H8.xml",
# "Ham.xml",
# "JC.xml",
# "Jn.xml",
# "LLL.xml",
# "Lr.xml", 
# "Luc.xml",
# "Mac.xml",
# "MM.xml",
# "MND.xml",
# "MV.xml",
# "Oth.xml",
# "Per.xml",
# "PhT.xml",
# "R2.xml",
# "R3.xml",
# "Rom.xml",
# "Shr.xml",
# "Son.xml",
# "TGV.xml",
# "Tim.xml",
# "Tit.xml",
# "Tmp.xml",
# "TNK.xml",
# "TN.xml",
# "Tro.xml",
# "Ven.xml",
# "Wiv.xml",
# "WT.xml",
]

d = Display("total_words", "chars_on_stage")
for play in all_plays: 
  c = CharsOnStage(Play(play))
  d.add_data(c.data, play)
  d.display()