from common.utils import clean_up_text

class WordAnalyzer():
    def __init__(self, play):
        self.play = play.data
        self._total_words = 0
        self.data = [] # results of calculation stored here
        self.calculate()

    def _handle_speech(self, e):
        char = e.getAttribute("who")
        wds = 0
        if char and char != "" and not char.isupper():
            if len(e.getElementsByTagName("ab")) > 0:
                wds = len(e.getElementsByTagName("ab")[0].getElementsByTagName("w"))
                self._total_words += wds
        return char, wds

    def calculate(self):
        acts = self.play.getElementsByTagName("div2")
        totals = []
        for i, act in enumerate(acts):
            actions = act.childNodes
            for j, action in enumerate(actions):
                wds = 0
                if action.nodeValue != "\n" and action.nodeValue != " \n":
                    try:
                        if action.tagName == "sp":
                            char, wds = self._handle_speech(action)
                    except AttributeError:
                        continue # some nodes are empty -- just ignore them
                    if wds != 0:
                        self.data.append([j, i, char, wds, self._total_words])
