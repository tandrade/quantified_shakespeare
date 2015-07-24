class BechdelTest():
    male = "1"
    female = "2"

    def __init__(self, play):
        self.play = play

    # return dictionary with character name as key,
    #    gender (M / F) as key
    def _get_genders(self):
        gender_map = {}
        char_list = self.play.data.getElementsByTagName("person")
        for char in char_list:
            nameObj = char.getElementsByTagName("name")
            genderObj = char.getElementsByTagName("sex")
            if nameObj and genderObj:
                if nameObj[0].childNodes:
                    name = nameObj[0].childNodes[0].data
                    gender = genderObj[0].getAttribute("value")
                    gender_map[name] = gender
        return gender_map

    # given a node, parse the speaker
    def _get_speaker(self, speaker_node):
        # TODO: parse the speaker
        return ""

    # return a list of names of who is speaking in a given scene
    def _parse_scenes(self, scene):
        scene_summary = []
        actions = scene.childNodes
        for action in actions:
            if action.nodeValue != "\n" and action.nodeValue != " \n":
                try:
                    if action.tagName == "sp":
                        speaker = self._get_speaker(action)
                        scene_summary += [speaker]
                except AttributeError:
                    pass # ignore this
        return scene_summary

    # Step 1: do women talk to each other?
    def analyze(self):
        scenes = self.play.data.getElementsByTagName("div2")
        totals = []
        character_gender_map = self._get_genders()
        # scene_breakdowns = []
        # for scene in scenes:
        #     speaker_list = []
        #     speakers = self._parse_scenes(scene)
        #     for speaker in speakers:
        #         if speaker in character_gender_map:
        #             speaker_list.append(character_gender_map[speaker])
        #     scene_breakdowns.append(speaker_list)


