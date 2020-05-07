from defs import *
from script import *
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

pos_noun_prefix = {"NN", "NNS", "NNP", "NNPS"}
pos_pronoun = {"PRP"}
pos_verb = {"VB", "VBD", "VBG", "VBP", "VBZ"} # exclude "VBN" - which is past pariciple(ex. taken)
PRONOUNS = {'I', 'you', 'he', 'she', 'it', 'we', 'you', 'they'}

def find_Antecedent(tagged_text, previous_convs):
    print("find_Antecedent")
    # print(f"tagged_text {tagged_text}")
    # print(f"previous {previous_convs}")

if __name__ == "__main__":
    f = open("./data/FROZEN.txt")
    script = parse_playscript(f)
    previous_conv_type = -1
    previous_2_conv = { CONV : [], SING : [], NARR : []}
    for cont in script.content:
        changed = False
        
        if isinstance(cont, TIMEPLACE):
            # print("TIME : {}, PLACE : {}".format(cont.time, cont.place))
            continue
        # cont.type : NARR, CONV, SING
        
        # print("NARR : {}".format(cont.text))
        tokenized_text = word_tokenize(cont.text)
        tagged_text = pos_tag(tokenized_text)
        # print(tokenized_text[:5])
        # print(tagged_text[:5])
        if previous_conv_type != cont.type:
            previous_2_conv[previous_conv_type] = []
            previous_2_conv[cont.type] = tagged_text
        else: # previous_conv_type == cont.type:
            if len(previous_2_conv[cont.type]) < 2:
                previous_2_conv[cont.type].append(tagged_text)
            else:
                previous_2_conv[cont.type][0] = previous_2_conv[cont.type][1]
                previous_2_conv[cont.type][1] = tagged_text
        
        previous_conv_type = cont.type
        modified_text = tokenized_text
        for i, word_and_tag in enumerate(tagged_text):
            word, tag  = word_and_tag
            if tag and word == 'I':
                modified_text[i] = cont.speak.name
                changed = True
            elif tag in pos_pronoun:
                find_Antecedent(tagged_text, previous_2_conv[cont.type])
                changed = True
                break
        
        cont.modified_text = TreebankWordDetokenizer().detokenize(modified_text).strip()
        if changed:
            print(f"cont.text : {cont.text} {len(cont.text)}")
            print(f"cont.modified_text : {cont.modified_text} {len(cont.modified_text)}")


        # raw : We're underwater looking up at it. A saw cuts through, heading right for us.
        # tokenized_text : ['We', "'re", 'underwater', 'looking', 'up']
        # tagged_text : [('We', 'PRP'), ("'re", 'VBP'), ('underwater', 'JJ'), ('looking', 'VBG'), ('up', 'RP')]
