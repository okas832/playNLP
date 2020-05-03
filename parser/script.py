from character import CHARACTER
from defs import CONV, SING, DESC
from defs import ON_NONE, ON_NARR, ON_CONV, ON_SING, EX_SING

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
#
# text - str
#   text data
# type - int
#   0 : conversation
#   1 : sing
#   2 : description
#   use defs.CONV, defs.SING, defs.DESC instead of number
# speak - CHARACTER
#   who is saying
# listen - CHATACTER or None
#   who is listening
# ref - list of CHARACTER
#   link of pronouns
class CONV():
    def __init__(self, text, type, cont, speak):
        self.text = text
        self.type = type
        self.cont = cont
        self.speak = speak
        self.listen = None
        self.ref = []

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

# parse_playscript
#   parse play script from file
#
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
    # EX_SING : expecting sing
    am_flag = ON_NONE

    conv = CONV()
    before_type = None
    while True:
        line = fp.readline()
        if line == "":  # EOF
            break
        elif line.startswith("                  "):  # conv or sing or sing title
            # TODO : parse conv, sing
            #        ingore page number
        elif line.startswith("   "):  # narrator or time & place 
            # TODO : parse narrator, time & place
            #        think how to handle conv in page 18
            #        time & place, narrator mixed text?
        else:  # title or etc - ignore
            continue

        print(am_flag, line)
        input()

if __name__ == "__main__":
    f = open("../test/FROZEN.txt")
    parse_playscript(f)
