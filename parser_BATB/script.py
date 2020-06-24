from character import *
from defs import *

# this is a script parser for Beauty and the Beast
# Need to keep this format to apply to other code

# class SCRIPT
#   data of script
#
# content - list of CONV, DESC, TIMEPLACE
#   parsed results
# character - list of CHARACTER
#   characters in the script
class SCRIPT():
    def __init__(self):
        self.content = []
        self.character = []

    # get_character_by_name
    #   check if the chacacter name already shown before
    #   return CHARACTER which has same character name if exist
    #   return None if not exist
    def get_character_by_name(self, character_name):
        fl = list(filter(lambda x: character_name == x.name, self.character))
        if len(fl) == 0:
            return None
        return fl[0]

    # append_content
    #   add contents of script
    def append_content(self, cont):
        if not isinstance(cont, CONV) \
                and not isinstance(cont, TIMEPLACE):
            raise TypeError("content can only have CONV, DESC, TIMEPLACE, not %s" % (type(cont)))
        self.content.append(cont)

    # append_character
    #   add new character
    def append_character(self, character):
        if not isinstance(character, CHARACTER):
            raise TypeError("character can only have CHARACTER, not %s" % (type(cont)))
        self.character.append(character)


# class CONV
#   data of conversation
#
# text - str
#   text data
# type - int
#   0 : conversation
#   1 : sing
#   2 : narrator
#   use defs.CONV, defs.SING, defs.NARR instead of number
# cont - boolean
#   is this continued?
# speak - CHARACTER
#   who is saying
# listen - CHATACTER or None
#   who is listening
# ref - list of CHARACTER
#   link of pronouns
class CONV():
    def __init__(self, text, type, cont, speak):
        self.text = text
        self.modified_text = text
        self.type = type
        self.cont = cont
        self.speak = speak
        self.time_index=-1
        self.listen = set()
        self.ref = set()

    def __repr__(self):
        return "<conv {}>".format(self.type)

# Not need timeplace... but keep the format

# class TIMEPLACE
#   data of scene heading
#
# place - str
#   place where scene begin
# time - str
#   time of scene, but not exact time(DAY, DAWN, NIGHT, ...)
class TIMEPLACE():
    def __init__(self, time, place):
        self.time = time
        self.place = place

    def __repr__(self):
        return "<timeplace>"


def parse_playscript(fp):
    script = SCRIPT()

    while True:
        line = fp.readline().strip()
        if line.startswith("Compiled by"):
            break
    fp.readline()

    am_flag = ON_NONE

    conv = None

    while True:
        line = fp.readline().rstrip()
        if line.find("</pre>") != -1:
            break
        elif line == "":
            continue
        elif line.startswith("              "):
            if am_flag != ON_NONE:
                conv.text += ("" if len(conv.text) == 0 else " ") + line.strip()
        elif line[0] == "(":
            # emote
            # Do we need this?
            while True:
                if line[-1] == ")":
                    break
                line = fp.readline().rstrip()
        else:
            if am_flag != ON_NONE:
                script.append_content(conv)
            try:
                character_name, line = line.split(":")
            except:
                conv.text += ("" if len(conv.text) == 0 else " ") + line.strip()
                continue
            line = line.strip()
            if character_name != "NARRATOR":
                character = script.get_character_by_name(character_name)
                if not character:
                    character = CHARACTER(character_name, "")
                    script.append_character(character)
                conv = CONV(line, CONV, False, character)
                am_flag = ON_CONV
            else:
                conv = CONV(line, NARR, False, None)
                am_flag = ON_NARR
    for conv in script.content:
        conv.text = re.sub(r" ?\([^)]+\)", "", conv.text)
    return script
if __name__ == "__main__":
    f = open("./data/BeautyAndTheBeast.txt")
    script = parse_playscript(f)
    """
    for cont in script.content:
        if cont.type == NARR:
            print("NARR : {}".format(cont.text))
        else:
            print("{} : {}".format(cont.speak.name, cont.text))
    """
    for char in script.character:
        print(char.name)
