class BechdelTest():
    male = "1"
    female = "2"

    def __init__(self, play):
        self.name_map = {}
        self.play = play

    # return dictionary with character name as key,
    #    gender (M / F) as key
    def _get_genders(self):
        gender_map = {}
        char_list = self.play.data.getElementsByTagName("person")
        for char in char_list:
            xml_id = char.getAttribute("xml:id")
            nameObj = char.getElementsByTagName("name")
            genderObj = char.getElementsByTagName("sex")
            if nameObj and genderObj:
                if nameObj[0].childNodes:
                    name = nameObj[0].childNodes[0].data
                    gender = genderObj[0].getAttribute("value")
                    gender_map[xml_id] = gender
                    self.name_map[xml_id] = name
        return gender_map

    # given a node, parse the speaker
    def _get_speaker(self, speaker_node):
        speaker_id = speaker_node.getAttribute("who")
        return speaker_id[1:]

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

        ## Part 1: how many female characters do these plays have?
        women = [g == "2" for g in character_gender_map.values()]
        if women.count(True) < 2:
            print "Failed the first part of the Bechdel test: " + self.play.title
        else:
            scene_breakdowns = []
            for scene in scenes:
                speaker_list = []
                speakers = self._parse_scenes(scene)
                for speaker in speakers:
                    if speaker in character_gender_map:
                        speaker_list.append(character_gender_map[speaker])
                scene_breakdowns.append(speaker_list)

        for scene in scene_breakdowns:
            women_talking = 0
            for char_talking in scene:
                if women_talking == 1 and char_talking == "2":
                    print "Women talking in a row."
                if char_talking == "2":
                    women_talking = 1



