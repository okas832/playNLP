#!/usr/bin/env python
# coding: utf-8

# In[86]:


import nltk
from nltk import word_tokenize, pos_tag, ne_chunk, Tree
from nltk.tokenize.treebank import TreebankWordDetokenizer


# In[87]:


def pp(sent):
    sent = word_tokenize(sent)
    sent = pos_tag(sent)
    return sent


# In[88]:


pp("KRISTOFF and SVEN are playing.")


# In[89]:


pp("KRISTOFF and SVEN are playing")


# In[90]:


pp("A sharp ice floe overtakes the workers, threateningly.")


# In[91]:


pp("Elsa shoves Anna off the bed. Anna lands butt to floor, sighs, defeated. But then she gets an idea. She hops back on the bed and lifts one of Elsa's eyelids.")


# In[92]:


# modified_text = [('KRISTOFF and SVEN', 'NNP'),
#  ('are', 'VBP'),
#  ('playing', 'VBG'),
#  ('.', '.')]
# modified_text = [('KRISTOFF', 'NNP'),
#  ('and', 'CC'),
#  ('SVEN', 'NNP'),
#  ('are', 'VBP'),
#  ('playing', 'VBG'),
#  ('.', '.')]
# result = TreebankWordDetokenizer().detokenize(modified_text).strip()
# result = detokenize(modified_text)
# result


# In[93]:


sents = ["Snowflakes suddenly burst forth and dance between her palms, forming a snowball."]
tagged_sents_list = [
    [[('I', 'PRP'), ('KNOW', 'VBP'), ('IT', 'NNP'), ('ALL', 'NNP'), ('ENDS', 'NNP'), ('TOMORROW', 'NNP'), (',', ','), ('SO', 'NNP'), ('IT', 'NNP'), ('HAS', 'NNP'), ('TO', 'NNP'), ('BE', 'NNP'), ('TODAY', 'NNP'), ('!', '.'), ('!', '.'), ('`', '``'), ('CAUSE', 'NN'), ('FOR', 'IN'), ('THE', 'NNP'), ('FIRST', 'NNP'), ('TIME', 'NNP'), ('IN', 'NNP'), ('FOREVER', 'NNP'), ('.', '.'), ('.', '.'), ('.', '.'), ('FOR', 'IN'), ('THE', 'NNP'), ('FIRST', 'NNP'), ('TIME', 'NNP'), ('IN', 'NNP'), ('FOREVER', 'NNP'), ('!', '.'), ('NOTHING', 'NN'), ("'S", 'VBZ'), ('IN', 'NNP'), ('MY', 'NNP'), ('WAY', 'NN'), ('!', '.'), ('!', '.'), ('!', '.')], [('(', '('), ('frustrated', 'VBN'), (')', ')'), ('Hey', 'NN'), ('!', '.')], [('(', '('), ('gentler', 'NN'), (')', ')'), ('Hey', 'NNP'), ('.', '.'), ('I-ya', 'NNP'), (',', ','), ('no', 'DT'), ('.', '.'), ('No', 'UH'), ('.', '.'), ('I', 'PRP'), ("'m", 'VBP'), ('okay', 'JJ'), ('.', '.')]],
    [[('Here', 'RB'), ('?', '.'), ('Are', 'VBP'), ('you', 'PRP'), ('sure', 'JJ'), ('?', '.')], [('Hi', 'NNP'), ('me', 'PRP'), ('...', ':'), ('?', '.'), ('Oh', 'UH'), ('.', '.'), ('Um', 'NNP'), ('.', '.'), ('Hi', 'NNP'), ('.', '.')], [('Thank', 'NNP'), ('you', 'PRP'), ('.', '.'), ('You', 'PRP'), ('look', 'VBP'), ('beautifuller', 'JJ'), ('.', '.'), ('I', 'PRP'), ('mean', 'VBP'), (',', ','), ('not', 'RB'), ('fuller', 'VB'), ('.', '.'), ('You', 'PRP'), ('do', 'VBP'), ("n't", 'RB'), ('look', 'VB'), ('fuller', 'NN'), (',', ','), ('but', 'CC'), ('more', 'JJR'), ('beautiful', 'NNS'), ('.', '.')]],
    [[('That', 'DT'), ("'s", 'VBZ'), ('horrible', 'JJ'), ('.', '.')], [('...', ':'), ('And', 'CC'), ('sisters', 'NNS'), ('.', '.'), ('Elsa', 'NNP'), ('and', 'CC'), ('I', 'PRP'), ('were', 'VBD'), ('really', 'RB'), ('close', 'JJ'), ('when', 'WRB'), ('we', 'PRP'), ('were', 'VBD'), ('little', 'JJ'), ('.', '.'), ('But', 'CC'), ('then', 'RB'), (',', ','), ('one', 'CD'), ('day', 'NN'), ('she', 'PRP'), ('just', 'RB'), ('shut', 'VB'), ('me', 'PRP'), ('out', 'RP'), (',', ','), ('and', 'CC'), ('I', 'PRP'), ('never', 'RB'), ('knew', 'VBD'), ('why', 'WRB'), ('.', '.')], [('Okay', 'NNP'), (',', ','), ('can', 'MD'), ('I', 'PRP'), ('just', 'RB'), ('say', 'VBP'), ('something', 'NN'), ('crazy', 'NN'), ('?', '.')]],
]


# In[94]:


for sent in sents:
    sent = pp(sent)
    t = ne_chunk(sent)
    sub = [subtree.leaves() for subtree in t if type(subtree) == Tree and subtree.label() == "NP"]
    if sub:
        print(t)
        print(sub)


# In[95]:


for tagged_sents in tagged_sents_list:
    for sent in tagged_sents:
        t = ne_chunk(sent)
        sub = [subtree.leaves() for subtree in t if type(subtree) == Tree and subtree.label() == "NP"]

        print(t)
        print(sub)
        print()


# In[96]:


def find_listeners_easy():
    moving_index=0
    for t_index in range(-1, timei):
        print(t_index)
        start_index=moving_index
        listeners=set()
        while(moving_index<len_of_script_contents):
            cont=script.content[moving_index]
            if(isinstance(cont, TIMEPLACE)):
                moving_index+=1
                break
            elif(cont.type==2):
                moving_index+=1
                continue
            else:
                listeners.add(cont.speak)
                moving_index+=1
        while(start_index<moving_index):
            cont=script.content[start_index]
            if(isinstance(cont, TIMEPLACE)):
                start_index+=1
                break
            elif(cont.type==2):
                start_index+=1
                continue
            listeners_cash=listeners.copy()
            listeners_cash.discard(cont.speak)
            cont.listen=listeners_cash
            start_index+=1 
            if(cont.listen != None):
                for person in cont.listen:
                    print(person.name)
                print("-----------")


index_of_listener_list=0
num_of_total_listeners=0
num_of_correct_listeners=0

def find_listeners_hard_with_using_weights():
    global num_of_total_listeners
    global num_of_correct_listeners
    global index_of_listener_list
    index_number=-1
    weight_for_searching_speaker=10
    weight_for_comparing_nearest=1
    for i in range(0, len_of_script_contents):
        cont=script.content[i]
        if(isinstance(cont, TIMEPLACE)):
            index_number+=1
        elif(cont.type==2):
            continue
        else:
            listeners=set()
            #print(index_number)
            for j in range(i-(int)(weight_for_searching_speaker/2), i+(int)(weight_for_searching_speaker/2)):
                if(j<0 or j>= len_of_script_contents):
                    continue
                cont_diff=script.content[j]
                if(isinstance(cont_diff, TIMEPLACE)):
                    if(j<i):
                        listeners=set()
                        continue
                    else:
                        break
                elif(cont_diff.type==2):
                    continue
                if(cont_diff.speak!=cont.speak):
                    if(len(cont_diff.speak.name)>6 and cont_diff.speak.name[:6]=="YOUNG "):
                        cont_diff.speak.name=cont_diff.speak.name[6:]
                    listeners.add(cont_diff.speak)
                if(abs(i-j)<=weight_for_comparing_nearest):
                    listeners=listeners|cont_diff.listen
                    listeners.discard(cont.speak)
            cont.listen=listeners
            if(index_of_listener_list<len(listeners_list)):
                num_of_total_listeners+=len(listeners_list[index_of_listener_list])
                if(len(cont.listen)==0):
                    num_of_total_listeners+=1
                    if(listeners_list[index_of_listener_list][0]==None):
                        num_of_correct_listeners+=1   
                else:
                    for lstn in cont.listen:
                        #print(lstn.name)
                        if(lstn.name in listeners_list[index_of_listener_list]):
                            num_of_correct_listeners+=1             
                #print(listeners_list[index_of_listener_list])
                #print("---------------------------")
                index_of_listener_list+=1


# In[97]:


from defs import *
from script import *
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from forevaluation import *
import string

pos_noun = {"NN", "NNS", "NNP", "NNPS"}
pos_single_noun = {"NN", "NNP"}
pos_plural_noun = {"NNS", "NNPS"}
# pos_noun = {"NN", "NNP"}
pos_pronoun = {"PRP", "PRP$"}
pos_verb = {"VB", "VBD", "VBG", "VBP", "VBZ"} # exclude "VBN" - which is past pariciple(ex. taken)
pure_indicating_verbs = {"discuss", "present", "illustrate", "identify", "summarise", "examine",
"describe", "define", "show", "check", "develop", "review", "report", "outline", "consider", "investigate", "explore", "assess",
"analyse", "synthesise", "study", "survey", "deal", "cover"}
indefinite_DT = {"a", "an", "many", "any", "either", "some"}

indicating_verbs  = set()
for verb in pure_indicating_verbs:
    indicating_verbs.add(verb)
    if verb.endswith("s"):
        indicating_verbs.add(verb+"es")
    else:
        indicating_verbs.add(verb+"s")
    
    if verb.endswith("e"):
        indicating_verbs.add(verb+"d")
    else:
        indicating_verbs.add(verb+"ed")
# cons = {"and", "or", "before", "after", "until", "when", "since", "while", "once", "as soon as", "as"}
# prepositions = {}
PRONOUNS = {"you", "they", "we", "us", "their", "your"}
SINGLE_PRONOUNS = {"you", "your"}
# PLURAL_PRONOUNS = {"they", "we", "us", "their"}
man_pronoun = {"he", "his", "him"}
woman_pronoun = {"she", "her"}
man = {"kristoff", "sven", "olaf", "hans", "king"}
woman = {"elsa", "anna", "queen"}


# global total_first
# global total_indicating
# global total_lexical
# global total_collocation

total_first = 0
total_indicating = 0
total_lexical = 0
total_collocation = 0
total_immediate = 0
total_referential = 0
total_preposition = 0
total_indefinite = 0
total_giveness = 0
# total_matches = [0 for _ in range(8)]


# In[98]:


def detokenize(tokens):
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

# Below two function is for calculate collocation match

def find_leftmost_verb(index, verb_word_and_tags):
    word = None
    for i, word_and_tag in verb_word_and_tags.items():
        if i < index: 
            word, _ = word_and_tag
        else:
            break
    return word

def find_rightmost_verb(index, verb_word_and_tags):
    for i, word_and_tag in verb_word_and_tags.items():
        if i < index: continue
        word, _ = word_and_tag
        return word
    return None

def find_noun_justbefore(index, _word_and_tags):
    word = None
    for i, word_and_tag in _word_and_tags.items():
        if i < index: 
            word, _ = word_and_tag
        else:
            break
    return word

def find_pronoun_justafter_con(index, pronoun_word_and_tags):
    for i, word_and_tag in pronoun_word_and_tags.items():
        if i < index: continue
        return i
    return None

def find_noun_justafter_indefiniteDT(index, available_nouns):
    for aidx, available_noun in enumerate(available_nouns):
        _, idx, _, _ = available_noun
        if idx > index:
            return aidx
    return None


# In[118]:


def find_Antecedent(text, tagged_text, previous_convs):
    print(f"find_Antecedent : {text}")
#     print("previous_convs")
#     print(previous_convs)
    global total_first
    global total_indicating
    global total_lexical
    global total_collocation
    global total_immediate
    global total_referential
    global total_preposition
    global total_indefinite
    global total_giveness
    # print("find_Antecedent")
    # print(tagged_text)
    modified_text = text
    # print(f"tagged_text {tagged_text}")
    # print(f"previous {previous_convs}")
    pronoun_word_and_tags = {}
    noun_word_and_tags = {}
    verb_word_and_tags = {}
    cons_word_and_tags = {}
    preposition_word_and_tags = {}
    indefinite_word_and_tags = {}

    noun_with_counts = {}
    predefined_verb_indicies = []
    for i, word_and_tag in enumerate(tagged_text):
        word, tag = word_and_tag
        if tag in pos_pronoun:
            pronoun_word_and_tags[i] = word_and_tag
        elif tag in pos_noun:
            noun_word_and_tags[i] = word_and_tag
            if noun_with_counts.get(word)==None:
                noun_with_counts[word] = 0
            noun_with_counts[word] += 1
        elif tag in pos_verb:
            verb_word_and_tags[i] = word_and_tag
        # elif word in cons:
        #     cons_word_and_tags[i] = word_and_tag
        elif tag=="CC":
            cons_word_and_tags[i] = word_and_tag
        elif tag=="IN":
            preposition_word_and_tags[i] = word_and_tag
        # elif tag=='DT' and word.lower() in indefinite_DT:
        #     indefinite_word_and_tags[i] = word_and_tag


        if word in indicating_verbs:
            predefined_verb_indicies.append(i)
    # print(f"previous_convs : {previous_convs}")
    prev_sentence_available_nouns = []
    prev_sentence_available_nouns_set = set()
    is_imperative_sentence = False
    
    for j, previous_conv in enumerate(previous_convs[::-1]):
        if j >= 2: break
        for i, word_and_tag in enumerate(previous_conv):
            word, tag = word_and_tag
            if tag=='DT' and word.lower() in indefinite_DT:
                indefinite_word_and_tags[i+100] = word_and_tag
            if tag in pos_noun:
                if word not in prev_sentence_available_nouns_set:
                    prev_sentence_available_nouns_set.add(word)
                    prev_sentence_available_nouns.append( [0, i+100, word, tag] )
            if j==0 and i==0 and tag in pos_verb:
                is_imperative_sentence = True

    # Giveness
    if not is_imperative_sentence:
        if prev_sentence_available_nouns:
            prev_sentence_available_nouns[0][0] += 1
            total_giveness += 1



    for j, previous_conv in enumerate(previous_convs):
        for i, word_and_tag in enumerate(previous_conv):
            word, tag = word_and_tag
            if tag not in pos_noun: continue
            if noun_with_counts.get(word)==None:
                noun_with_counts[word] = 0
            noun_with_counts[word] += 1
            
    for i, word_and_tag in enumerate(tagged_text):
        word, tag = word_and_tag
        if tag not in pos_noun: continue
        if noun_with_counts.get(word)==None:
            noun_with_counts[word] = 0
        noun_with_counts[word] += 1
    # print(f"pronoun_word_and_tags : {pronoun_word_and_tags}")
    # print(f"noun_word_and_tags : {noun_word_and_tags}")

    for index, word_and_tag in pronoun_word_and_tags.items():
        available_nouns = []
        available_nouns_set = set()
        word, tag = word_and_tag
        for idx, wnt in noun_word_and_tags.items():
            w, t = wnt
            # print(f"idx : {idx} index : {index} w : {w} word : {word}")
            if idx < index and ((w.lower() in man and word.lower() in man_pronoun) or (w.lower() in woman and word.lower() in woman_pronoun)                 or (word.lower() in SINGLE_PRONOUNS)):
                if w not in available_nouns_set:
                    available_nouns_set.add(w)
                    available_nouns.append( [0, idx, w, t] )
                    
        
        
        # Add prev_sentence noun if the noun does not appear in current sentence
        for p_available_noun in prev_sentence_available_nouns:
            s, idx, w, t = p_available_noun
            if ((w.lower() in man and word.lower() in man_pronoun) or (w.lower() in woman and word.lower() in woman_pronoun)                     or (word.lower() in SINGLE_PRONOUNS)):
                if w not in available_nouns_set:
                    available_nouns_set.add(w)
                    available_nouns.append( [s, idx, w, t] )
#         if available_nouns:
#             prev_available_nouns = []
#             for available_noun in available_nouns:
#                 _, _, w, t = available_noun
#                 for prev_sentence_available_noun in prev_sentence_available_nouns:
#                     _, _, pw, _ = prev_sentence_available_noun
#                     if w!=pw:
#                         available_nouns_set.add(pw)
#                         prev_available_nouns.append(prev_sentence_available_noun)
#                         break
#             available_nouns.extend(prev_available_nouns)
#         else:
#             available_nouns = prev_sentence_available_nouns
        
#         print("prev_available_nouns")
#         print(prev_available_nouns)
        print("available_nouns")
        print(available_nouns)
        # print("target word")
        # print(word)
        # print("available_nouns")
        # print(available_nouns)
        if len(available_nouns) == 0: continue
        
        available_nouns.sort(key=lambda x:x[1])
        
        # First noun phase
        if available_nouns[0][1] < 100:
            available_nouns[0][0] += 1
            total_first += 1
            
        # Indicating verbs
        for predefined_verb_index in predefined_verb_indicies:
            for available_noun in available_nouns:
                if available_noun[1] > predefined_verb_index:
                    available_noun[0] += 1
                    total_indicating += 1
                    break
        # Lexical reiteration
        for available_noun in available_nouns:
            if noun_with_counts.get(available_noun[2])==None:
                continue
            if noun_with_counts[available_noun[2]] >= 2:
                available_noun[0] += 2
                total_lexical += 1
            elif noun_with_counts[available_noun[2]] >= 2:
                available_noun[0] += 1
                total_lexical += 1
        # Collocation match
        for available_noun in available_nouns:
            _, idx, _, _ = available_noun
            if find_leftmost_verb(index, verb_word_and_tags) == find_leftmost_verb(idx, verb_word_and_tags) or                 find_rightmost_verb(index, verb_word_and_tags) == find_rightmost_verb(idx, verb_word_and_tags):
                available_noun[0] += 2
                total_collocation += 1
        # Immediate reference
        for cidx, word_and_tag in cons_word_and_tags.items():
            if index == find_pronoun_justafter_con(cidx, pronoun_word_and_tags):
                for available_noun in available_nouns:
                    _, idx, available_word, tag = available_noun
                    if available_word == find_noun_justbefore(cidx, noun_word_and_tags):                    
                        available_noun[0] += 2
                        total_immediate += 1
        # Referential distance
        for j, previous_conv in enumerate(previous_convs[::-1]):
            if j==3: break
            for available_noun in available_nouns:
                _, idx, available_word, t = available_noun
                # print("previous_conv")
                # print(previous_conv)
                # print("(available_word, tag)")
                # print(f"({available_word}, {tag})")
                if (available_word, t) in previous_conv:
                    available_noun[0] += 1-j
                    total_referential += 1
        
        # Non-prepositional pharse
        for pidx, word_and_tag in preposition_word_and_tags.items():
            for available_noun in available_nouns:
                _, idx, available_word, _ = available_noun
                if available_word == find_noun_justbefore(pidx, noun_word_and_tags):                    
                    available_noun[0] -= 1
                    total_preposition += 1
        
        # Definiteness
        for iidx, word_and_tag in indefinite_word_and_tags.items():
            aidx = find_noun_justafter_indefiniteDT(iidx, available_nouns)
            if aidx:
                available_nouns[aidx][0] -= 1
                total_indefinite += 1

        

        
        available_nouns.sort(reverse=True)
        print("target word")
        print(pronoun_word_and_tags[index])
        print("available_nouns")
        print(available_nouns)
        # print(f"target anaphora : {text[index]}")
        # print("available_nouns")
        # print(available_nouns)
        # print(f"tagged_text[index][1] : {tagged_text[index][1]}")
        if tagged_text[index][1] == "PRP" and tagged_text[index][0] in PRONOUNS and len(available_nouns) >= 2:
            del modified_text[index]
            modified_text = modified_text[:index] + [available_nouns[0][2], "and", available_nouns[1][2]] +modified_text[index:]
        elif tagged_text[index][1] == "PRP":
            # print(f"{modified_text[index]} <==== {available_nouns[0][2]}")
            modified_text[index] = available_nouns[0][2]
        else: # PRP$
            # print(f"{modified_text[index]} <==== {available_nouns[0][2]}\'s ")
            modified_text[index] = available_nouns[0][2] + '\'s'
#     print("modified_text")
#     print(modified_text)
    return modified_text


# In[119]:


if __name__ == "__main__":
    f = open("./data/FROZEN.txt")
    script = parse_playscript(f)
    previous_conv_type = -1
    previous_type_conv = { CONV : [], SING : [], NARR : []}
    
    num_of_total_modified = 0
    num_of_correctly_modified = 0

    all_characters = set()
    for cont in script.content:
        if isinstance(cont, CONV):
            if isinstance(cont.speak, CHARACTER):
                all_characters.add(cont.speak.name)
    previous_character_conv = dict()
    for character in all_characters:
        previous_character_conv[character] = []

    for cont in script.content:
        
        changed = False
       
        
        if isinstance(cont, TIMEPLACE):
            # print("TIME : {}, PLACE : {}".format(cont.time, cont.place))
            previous_type_conv = { CONV : [], SING : [], NARR : []}
            previous_conv_type = -1
            for character in all_characters:
                previous_character_conv[character] = []
            continue
        # cont.type : NARR, CONV, SING
        
        
        texts = cont.text.split(".")
        modified_texts = []
        previous_convs = []
        if isinstance(cont, CONV):
            if isinstance(cont.speak, CHARACTER): 
                previous_convs = previous_character_conv[cont.speak.name]
            else:
                previous_convs = previous_type_conv[cont.type]
        else:
            previous_convs = previous_type_conv[cont.type]
        
        for text in texts:
            tokenized_text = word_tokenize(text)
            tagged_text = pos_tag(tokenized_text)


            modified_text = tokenized_text

            for i, word_and_tag in enumerate(tagged_text):
                word, tag  = word_and_tag
                # if tag and (word == 'I' or word=="me" or word=="Me"):
                #     if word=='I' and tagged_text[i+1][0] == "\'m":
                #         modified_text[i+1] = "is"    
                #     # print(f"cont.text : {cont.text} {len(cont.text)}")
                #     modified_text[i] = cont.speak.name
                #     changed = True
                if tag in pos_pronoun:
                        
                    modified_text = find_Antecedent(tokenized_text, tagged_text, previous_convs)
                    changed = True    
                    
                    break
#             print(f"lst : {modified_text}")
            modified_text = TreebankWordDetokenizer().detokenize(modified_text).strip()
#             print(f"2nd : {modified_text}")
            modified_texts.append(modified_text)
#         print("***modified_texts***")
#         print(modified_texts)
            previous_convs.append(tagged_text)
    
    
    
        if len(modified_texts) >= 2:
            cont.modified_text = ". ".join(modified_texts).strip()
        else:
            cont.modified_text = modified_texts[0] + "."
#         if len(modified_texts) >= 2:
#             modified_text = ". ".join(modified_texts)
#         cont.modified_text = TreebankWordDetokenizer().detokenize(modified_text).strip()
#         cont.modified_text= detokenize(modified_text)
        if changed:
            if(num_of_total_modified<len(modified_texts_list)):
                #print(cont.modified_text)
                #print(modified_texts_list[num_of_total_modified][0])
                #print()
                print(f"{num_of_total_modified+1}")
                print("text")
                print(f"{cont.text} {len(cont.text)}")
                print("modified_text")
                print(f"{cont.modified_text} {len(cont.modified_text)}")
                print("answer")
                print(f"{modified_texts_list[num_of_total_modified][0]} {len(modified_texts_list[num_of_total_modified][0])}")
                if(cont.modified_text==modified_texts_list[num_of_total_modified][0]):
                    print("--------------- Correct ! -----------------------")
                    num_of_correctly_modified+=1
                num_of_total_modified+=1

    #evaluation
    print("Modified text correctness:"+str(num_of_correctly_modified)+"/"+str(num_of_total_modified))
    
    #Finding listeners by sdh
    len_of_script_contents=len(script.content)
    timei=-1
    for index in range(0,len_of_script_contents):
        cont=script.content[index]
        if(isinstance(cont, TIMEPLACE)):
            timei+=1
        else:
            cont.time_index=timei
    
    find_listeners_hard_with_using_weights()

    #evaluation
    print("Listeners match correctness:"+str(num_of_correct_listeners)+"/"+str(num_of_total_listeners))
    

    # raw : We're underwater looking up at it. A saw cuts through, heading right for us.
    # tokenized_text : ['We', "'re", 'underwater', 'looking', 'up']
    # tagged_text : [('We', 'PRP'), ("'re", 'VBP'), ('underwater', 'JJ'), ('looking', 'VBG'), ('up', 'RP')]

    # How many match ?
    print(f"total_first : {total_first}")
    print(f"total_indicating : {total_indicating}")
    print(f"total_lexical : {total_lexical}")
    print(f"total_collocation : {total_collocation}")
    print(f"total_immediate : {total_immediate}")
    print(f"total_referential : {total_referential}")
    print(f"total_preposition : {total_preposition}")
    print(f"total_indefinite : {total_indefinite}")
    print(f"total_giveness : {total_giveness}")
    

    


# In[ ]:





# In[ ]:




