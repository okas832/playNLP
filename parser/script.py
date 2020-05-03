from character import CHARACTER
from defs import CONVERSATION, SING
from defs import ON_NONE, ON_NARR, ON_CONV, ON_SING

# class SCRIPT
#   data of script
# content - list of CONV, DESC, TIMEPLACE
#   parsed results
# character - list of CHARACTER
#   characters in the script
class SCRIPT():
    def __init__(self):
        self.content = []
        self.character = []

    # is_character_name_already_shown
    #   check if the chacacter name already shown before
    #   return CHARACTER which has same character name if exist
    #   return None if not exist
    def is_character_name_already_shown(self, character_name):
        fl = filter(lambda x: character_name == x.name, self.character)
        if len(fl) == 0:
            return None
        return fl[0]

    # append_content
    #   add contents of script
    def append_content(self, cont):
        if not isinstance(cont, CONV)\
       and not isinstance(cont, DESC)\
       and not isinstance(cont, TIMEPLACE):
            raise TypeError("content can only have CONV, DESC, TIMEPLACE, not %s"%(type(cont)))
        self.content.append(cont)
    # append_character
    #   add new character
    def append_character(self, character):
        if not isinstance(character, CHARACTER):
            raise TypeError("character can only have CHARACTER, not %s"%(type(cont)))
        self.character.append(character)

# class CONV
#   data of conversation
# text - str
#   text data
# type - int
#   0 : conversation
#   1 : sing
# speak - CHARACTER
#   who is saying
# listen - CHATACTER or None
#   who is listening
# ref - list of CHARACTER
#   link of pronouns
class CONV():
    def __init__(self, text, type, speak):
        self.text = text
        self.type = type
        self.speak = speak
        self.listen = None
        self.ref = []

# class DESC
#   data of narrator
# text - str
#   text data
class DESC():
    def __init__(self, text):
        self.text = text

# class TIMEPLACE
#   data of scene heading
# place - str
#   place where scene begin
# time - str
#   time of scene, but not exact time(DAY, DAWN, NIGHT, ...)
class TIMEPLACE():
    def __init__(self, place, time):
        self.place = place
        self.time = time

# parse_playscript
#   parse play script from file
# input
#   fp - File Object
#     file pointer to read
# output
#   SCRIPT Object
#     result of parsing script
def parse_playscript(fp):
    script = SCRIPT()

    # find first line
    # *in lazy way*
    while True:
        line = fp.readline().strip()
        if line.startswith("   OPEN ON: "):
            break

    script.append_content(DESC(line.split("OPEN ON: ")[1], None))

    # automata flag
    # ON_NONE : expecting everything
    # ON_NARR : on narrator
    # ON_CONV : on normal conversation
    # ON_SING : on sing
    am_flag = 0

    conv = CONV()
    while True:
        line = fp.readline()
        if line == "":  # EOF
            break
        elif line == "\n":  # blank line
            am_flag = ON_NONE
        elif line.startswith("    "):  # conv or sing
            #  TODO: handle conv or sing
            #        ignore page number
            pass
        elif line.startswith("   "):  # narrator
            #  TODO: handle narrator
            pass
        else:  # title or etc - ignore
            continue












