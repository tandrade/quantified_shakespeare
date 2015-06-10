import xml.dom.minidom as minidom
import pandas as pd
from ggplot import *

class Play:
  def __init__(self, xml_file):
    self.data = minidom.parse(xml_file)

#FIXME: schema has changed
class Display():
  title_column_name = "title"
  file_column_name = "filename"

  def __init__(self, x_label, y_label, x_max=None, y_max=None, x_display="", y_display=""):
    self.y_label = y_label
    self.x_label = x_label
    self.x_max = x_max
    self.y_max = y_max
    self.x_display = x_display
    self.y_display = y_display
    self.agg_data = []

  # note: assumes two variables - x as first, y as second
  def add_data(self, data, filename, label):
    self.agg_data += [[d[0], d[1], filename, label] for d in data]

  # removing duplicate x, value pairs: take the last chronological value, skip 0s
  # TODO: is there a more efficient way to do this?
  def _clean_data(self):
    prev_x = 0
    cleaned_data = []
    for row in list(reversed(self.agg_data)):
      if row[0] == 0:
        continue
      if row[0] != prev_x:
        cleaned_data += [row]
      prev_x = row[0]
    self.agg_data = list(reversed(cleaned_data))


  def display(self, max_x=None, max_y=None):
    self._clean_data()
    df = pd.DataFrame(self.agg_data, columns=[self.x_label , self.y_label, self.file_column_name,
                                              self.title_column_name])
    gg = ggplot(aes(x = self.x_label, ymin=0, ymax=self.y_label), data=df) + geom_area()
    if self.x_max:
      gg = gg + xlim(0, self.x_max)
    if self.y_max:
      gg = gg + ylim(0, self.y_max)
    if self.x_display:
      gg = gg + xlab(self.x_display)
    if self.y_display:
      gg = gg + ylab(self.y_display)
    gg = gg + facet_grid(self.title_column_name)
    print gg