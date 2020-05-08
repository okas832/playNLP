from defs import *
from script import *
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

pos_noun = {"NN", "NNS", "NNP", "NNPS"}
pos_pronoun = "PRP"
pos_verb = {"VB", "VBD", "VBG", "VBP", "VBZ"} # exclude "VBN" - which is past pariciple(ex. taken)
Verb_set = {"discuss", "present", "illustrate", "identify", "summarise", "examine",
"describe", "define", "show", "check", "develop", "review", "report", "outline", "consider", "investigate", "explore", "assess",
"analyse", "synthesise", "study", "survey", "deal", "cover"},
# PRONOUNS = {'I', 'you', 'he', 'she', 'it', 'we', 'you', 'they'}

def find_Antecedent(text, tagged_text, previous_convs):
    # print("find_Antecedent")
    modified_text = text
    # print(f"tagged_text {tagged_text}")
    # print(f"previous {previous_convs}")
    pronoun_word_and_tags = {}
    noun_word_and_tags = {}
    noun_with_counts = {}
    predefined_verb_indicies = []
    for i, word_and_tag in enumerate(tagged_text):
        word, tag = word_and_tag
        if tag==pos_pronoun:
            pronoun_word_and_tags[i] = word_and_tag
        elif tag in pos_noun:
            noun_word_and_tags[i] = word_and_tag
            if noun_with_counts.get(word)==None:
                noun_with_counts[word] = 0
            noun_with_counts[word] += 1

        if word in Verb_set:
            predefined_verb_indicies.append(i)
    # print(f"previous_convs : {previous_convs}")

    for j, previous_conv in enumerate(previous_convs):
        for i, word_and_tag in enumerate(previous_conv):
            word, tag = word_and_tag
            if noun_with_counts.get(word)==None:
                noun_with_counts[word] = 0
            noun_with_counts[word] += 1
    # print(f"pronoun_word_and_tags : {pronoun_word_and_tags}")
    # print(f"noun_word_and_tags : {noun_word_and_tags}")

    for index, word_and_tag in pronoun_word_and_tags.items():
        available_nouns = []
        for idx, wnt in noun_word_and_tags.items():
            w, t = wnt
            if idx < index:
                available_nouns.append( [0, idx, w, t] )
        
        if len(available_nouns) == 0: continue
        # First noun phase
        available_nouns[0][0] += 1
        # Indicating verbs
        available_nouns.sort(key=lambda x:x[1])
        for predefined_verb_index in predefined_verb_indicies:
            for available_noun in available_nouns:
                if available_noun[1] > predefined_verb_index:
                    available_noun[0] += 1
                    break
        # Lexical reiteration
        for available_noun in available_nouns:
            if noun_with_counts.get(available_noun[2])==None:
                continue
            if noun_with_counts[available_noun[2]] >= 2:
                available_noun[0] += 2
            elif noun_with_counts[available_noun[2]] >= 2:
                available_noun[0] += 1
        available_nouns.sort(reverse=True)
        # print(f"available_nouns : {available_nouns}")
        modified_text[index] = available_nouns[0][2]
    
    return modified_text
if __name__ == "__main__":
    f = open("./data/FROZEN.txt")
    script = parse_playscript(f)
    previous_conv_type = -1
    previous_type_conv = { CONV : [], SING : [], NARR : []}
    for cont in script.content:
        changed = False
        
        if isinstance(cont, TIMEPLACE):
            # print("TIME : {}, PLACE : {}".format(cont.time, cont.place))
            previous_type_conv = { CONV : [], SING : [], NARR : []}
            previous_conv_type = -1
            continue
        # cont.type : NARR, CONV, SING
        
        # print("NARR : {}".format(cont.text))
        tokenized_text = word_tokenize(cont.text)
        tagged_text = pos_tag(tokenized_text)
        # print(tokenized_text[:5])
        # print("tagged_text")
        # print(tagged_text)
        
        
        modified_text = tokenized_text
        for i, word_and_tag in enumerate(tagged_text):
            word, tag  = word_and_tag
            if tag and word == 'I':
                modified_text[i] = cont.speak.name
                changed = True
            elif tag in pos_pronoun:
                modified_text = find_Antecedent(tokenized_text, tagged_text, previous_type_conv[cont.type])
                changed = True
                break
        
        cont.modified_text = TreebankWordDetokenizer().detokenize(modified_text).strip()
        if changed:
            print(f"cont.text : {cont.text} {len(cont.text)}")
            print(f"cont.modified_text : {cont.modified_text} {len(cont.modified_text)}")
            print()
        if previous_conv_type != cont.type:
            if previous_conv_type != -1:
                previous_type_conv[previous_conv_type] = []
            previous_type_conv[cont.type] = [tagged_text]
        else: # previous_conv_type == cont.type:
            previous_type_conv[cont.type].append(tagged_text)
            
        
        
        
        previous_conv_type = cont.type


        # raw : We're underwater looking up at it. A saw cuts through, heading right for us.
        # tokenized_text : ['We', "'re", 'underwater', 'looking', 'up']
        # tagged_text : [('We', 'PRP'), ("'re", 'VBP'), ('underwater', 'JJ'), ('looking', 'VBG'), ('up', 'RP')]
