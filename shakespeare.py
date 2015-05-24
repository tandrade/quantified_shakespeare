import xml.dom.minidom as minidom
import pandas as pd
import matplotlib.pyplot as mpl

henry_iv = minidom.parse("1H4.xml")

## First step: parse the characters 
'''
all_chars = []
# find lists of characters
cast_lists = henry_iv.getElementsByTagName("listPerson")
for cast_list in cast_lists:
  # find the people in those lists 
  char_nodes = cast_list.getElementsByTagName("person")
  for char_node in char_nodes:
    # all major characters will have the 'name' node, can get the data from there
    # minor characters don't follow this convention -- skipping them
    names = char_node.getElementsByTagName("name")
    if names:
      all_chars.append(names[0].childNodes[0].data)
'''

### Plot entrances by word
def handle_stage_events(e, chars_on_stage):
  e_type = e.getAttribute("type")
  update_value = 0
  chars = [char for char in e.getAttribute("who").split("#")]
  for c in chars:
    if c == "" or c.isupper():
      chars.remove(c)
  if e_type == "entrance":
    for char in chars:
      if char.strip() not in chars_on_stage:
        chars_on_stage.add(char.strip())
        update_value += 1
  if e_type == "exit":
    for char in chars:
      if char.strip() in chars_on_stage:
        chars_on_stage.remove(char.strip())
        update_value -= 1
  return chars_on_stage, update_value


def handle_speech(e, total_words, chars_on_stage):
  char = e.getAttribute("who")[1:] # remove hashtag
  update_value = 0
  if char and char != "" and not char.isupper():
    if char.strip() not in chars_on_stage:
      chars_on_stage.add(char.strip())
      update_value += 1
  wds = len(e.getElementsByTagName("ab")[0].getElementsByTagName("w"))
  total_words += wds
  return total_words, chars_on_stage, update_value

acts = henry_iv.getElementsByTagName("div2")
total_words = 0
totals = []
for act in acts:
  chars_on_stage = set()
  total_chars = 0
  actions = act.childNodes
  for action in actions:
    update = 0
    if action.nodeValue != "\n":
      if action.tagName == "stage":
        chars_on_stage, update = handle_stage_events(action, chars_on_stage)
      if action.tagName == "sp":
        total_words, chars_on_stage, update = handle_speech(action, total_words, chars_on_stage)
    if update != 0:
      total_chars += update
      if total_chars != 0:
        totals.append([total_chars, total_words])

df = pd.DataFrame(totals, columns=["total_chars", "total_words"])
df.plot(x="total_words", y="total_chars")
mpl.show()

