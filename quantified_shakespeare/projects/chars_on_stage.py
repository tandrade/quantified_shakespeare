from common.utils import clean_up_text

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
        for i, act in enumerate(acts):
            self._chars_on_stage = set() # reset who is on stage every act
            total_chars = 0
            actions = act.childNodes
            for j, action in enumerate(actions):
                update = 0
                type = ""
                if action.nodeValue != "\n" and action.nodeValue != " \n":
                    try:
                        if action.tagName == "stage":
                            update = self._handle_stage_events(action)
                            type = "stage"
                        if action.tagName == "sp":
                            update = self._handle_speech(action)
                            type = "speech"
                    except AttributeError:
                        print action.nodeValue # should not be called: log the issue
                if update != 0:
                    total_chars += update
                    if total_chars != 0:
                        self.data.append([j, i, type, self._total_words, total_chars])