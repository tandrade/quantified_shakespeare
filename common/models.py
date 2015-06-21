import xml.dom.minidom as minidom
import pandas as pd
import vincent
from ggplot import *

class Play:
    def __init__(self, xml_file, title, genre):
        self.data = minidom.parse(xml_file)
        self.title = title
        self.genre = genre


class DataAssembler():
    play_column_name = "play_label"

    def __init__(self, col_names):
        self.df = None
        self._agg_data = []
        self.column_names = col_names

    def add_data_to_parse(self, data, play_label):
        self._agg_data += [d + [play_label] for d in data]

    def create_matrix(self):
        self.column_names.append(self.play_column_name)
        self.matrix = pd.DataFrame(self._agg_data, columns=self.column_names)


class FacetedLineChart():

    def __init__(self, df, x_col, y_col, facet_field):
        self.df = df
        self.x_col = x_col
        self.y_col = y_col
        self.to_facet_on = facet_field

    def display(self, max_x=None, max_y=None):
        gg = ggplot(aes(x = self.x_col, ymin=0, ymax=self.y_col), data=self.df) + geom_area()
        if max_x:
            gg = gg + xlim(0, max_x)
        if max_y:
            gg = gg + ylim(0, max_y)
        gg = gg + facet_grid(self.to_facet_on)


class BarGraphDisplay():
    def __init__(self, df, x_col, y_col):
        self.df = df
        self.x_col = x_col
        self.y_col = y_col
        self.json_name = "bar.json"
        self.output_html_name = "test.html"

    def display(self):
        bar = vincent.Bar(list(self.df[self.x_col]), list(self.df[self.y_col]))
        bar.to_json(self.json_name, html_out=True, html_path=self.output_html_name)