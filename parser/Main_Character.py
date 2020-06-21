from script import *

main_property=100
weight_of_num_of_convs=1
weight_of_num_of_relations=5

def finding_main_characters(input_relations, script):
    output_hubos={}
    output=[]
    output_all=[]
    for character in script.character:
        output_hubos[character.name]=[0, 0]
    for conv in script.content:
        if(isinstance(conv, CONV)):
            if(conv.speak!=None and conv.speak.name in output_hubos.keys()):
                output_hubos[conv.speak.name][1]+=1
            elif(conv.speak!=None):
                output_hubos[conv.speak.name]=[0, 0]
    for charac in input_relations.keys():
        output_hubos[charac][0]+=len(input_relations[charac])
    for charac in output_hubos.keys():
        calculated_property=output_hubos[charac][0]*weight_of_num_of_relations+output_hubos[charac][1]*weight_of_num_of_convs
        if(main_property<calculated_property):
            output.append((charac, calculated_property))
        output_all.append((charac, calculated_property))
    output.sort(key=lambda x:x[1])
    output_all.sort(key=lambda x:x[1])
    output.reverse()
    output_all.reverse()
    return [output, output_all]
