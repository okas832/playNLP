from defs import *
from script import *
from Main_Character import *
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from forevaluation import *
import string
from relationship import Analyzer

# pos_noun = {"NN", "NNS", "NNP", "NNPS"}
pos_noun = {"NN", "NNP"}
pos_pronoun = {"PRP", "PRP$"}
pos_verb = {"VB", "VBD", "VBG", "VBP", "VBZ"} # exclude "VBN" - which is past pariciple(ex. taken)
Verb_set = {"discuss", "present", "illustrate", "identify", "summarise", "examine",
"describe", "define", "show", "check", "develop", "review", "report", "outline", "consider", "investigate", "explore", "assess",
"analyse", "synthesise", "study", "survey", "deal", "cover"},
# PRONOUNS = {'I', 'you', 'he', 'she', 'it', 'we', 'you', 'they'}
man_pronoun = {"he", "his", "him", "He", "His", "Him"}
woman_pronoun = {"she", "her", "She", "Her"}
man = {"Kristoff", "KRISTOFF", "Sven", "SVEN", "Olaf", "OLAF"}
woman = {"ELSA", "Elsa", "ANNA", "Anna"}

def detokenize(tokens):
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

def find_Antecedent(text, tagged_text, previous_convs):
    # print("find_Antecedent")
    # print(tagged_text)
    modified_text = text
    # print(f"tagged_text {tagged_text}")
    # print(f"previous {previous_convs}")
    pronoun_word_and_tags = {}
    noun_word_and_tags = {}
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
        word, tag = word_and_tag
        if (word not in man_pronoun) and (word not in woman_pronoun):
            # print(f"word : {word} continue")
            continue
        
        for idx, wnt in noun_word_and_tags.items():
            w, t = wnt
            # print(f"idx : {idx} index : {index} w : {w} word : {word}")
            if idx < index and ((w in man and word in man_pronoun) or (w in woman and word in woman_pronoun)):
                available_nouns.append( [0, idx, w, t] )
        # print("available_nouns")
        # print(f"{available_nouns}")
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
        # print(f"tagged_text[index][1] : {tagged_text[index][1]}")
        if tagged_text[index][1] == "PRP":
            # print(f"{modified_text[index]} <==== {available_nouns[0][2]}")
            modified_text[index] = available_nouns[0][2]
        else: # PRP$
            # print(f"{modified_text[index]} <==== {available_nouns[0][2]}\'s ")
            modified_text[index] = available_nouns[0][2] + '\'s'
    
    return modified_text

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



if __name__ == "__main__":
    f = open("./data/FROZEN.txt")
    script = parse_playscript(f)
    previous_conv_type = -1
    previous_type_conv = { CONV : [], SING : [], NARR : []}
    num_of_total_modified = 0
    num_of_correctly_modified = 0
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
            if tag and (word == 'I' or word=="me" or word=="Me"):
                if word=='I' and tagged_text[i+1][0] == "\'m":
                    modified_text[i+1] = "is"    
                # print(f"cont.text : {cont.text} {len(cont.text)}")
                modified_text[i] = cont.speak.name
                changed = True
            if tag in pos_pronoun:
                # print(f"word {word} tag {tag}")
                modified_text = find_Antecedent(tokenized_text, tagged_text, previous_type_conv[cont.type])
                changed = True    
                break
        cont.modified_text = TreebankWordDetokenizer().detokenize(modified_text).strip()
        cont.modified_text= detokenize(modified_text)
        if changed:
            if(num_of_total_modified<len(modified_texts_list)):
                #print(cont.modified_text)
                #print(modified_texts_list[num_of_total_modified][0])
                #print()
                # print(f"{num_of_total_modified+1}")
                # print("text")
                # print(f"{cont.text} {len(cont.text)}")
                # print("modified_text")
                # print(f"{cont.modified_text} {len(cont.modified_text)}")
                # print("answer")
                # print(f"{modified_texts_list[num_of_total_modified][0]} {len(modified_texts_list[num_of_total_modified][0])}")
                if(cont.modified_text==modified_texts_list[num_of_total_modified][0]):
                    num_of_correctly_modified+=1
                num_of_total_modified+=1

                # print(f"cont.text : {cont.text} {len(cont.text)}")
                # print(f"cont.modified_text : {cont.modified_text} {len(cont.modified_text)}")

        if previous_conv_type != cont.type:
            if previous_conv_type != -1:
                previous_type_conv[previous_conv_type] = []
            previous_type_conv[cont.type] = [tagged_text]
        else: # previous_conv_type == cont.type:
            previous_type_conv[cont.type].append(tagged_text)

        
        previous_conv_type = cont.type

        

    #evaluation
    #print("Modified text correctness:"+str(num_of_correctly_modified)+"/"+str(num_of_total_modified))
    
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
    #print("Listeners match correctness:"+str(num_of_correct_listeners)+"/"+str(num_of_total_listeners))
            
        # raw : We're underwater looking up at it. A saw cuts through, heading right for us.
        # tokenized_text : ['We', "'re", 'underwater', 'looking', 'up']
        # tagged_text : [('We', 'PRP'), ("'re", 'VBP'), ('underwater', 'JJ'), ('looking', 'VBG'), ('up', 'RP')]


#------------------------------------Analyzer----------------------------------------------------

    relationship_analyzer = Analyzer(script)
    relationship_analyzer.run()
    character_ranking=finding_main_characters(relationship_analyzer.relationship, script)
    print("Main Character: "+ str(character_ranking[0]))
    print("All Character ranking: "+str(character_ranking[1]))
    #import pdb; pdb.set_trace() #if you want to debug
