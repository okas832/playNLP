from nltk.sentiment.vader import SentimentIntensityAnalyzer
from script import TIMEPLACE
from collections import defaultdict
from nltk.tokenize import word_tokenize
import nltk
import re
import pickle
import networkx as nx

"""
class Analyzer: calculate sentiment, lovingness, and servant relationship scores between characters.
to use, please call analyzer at the end of anaphora_resolution.py.
and run: python3 anaphora_resolution.py

"""


class Analyzer():
    def __init__(self, script, divide_time=3):
        self.vader = SentimentIntensityAnalyzer()
        self.script = script
        self.relationship = defaultdict(dict)
        self.relationship_per_act = [defaultdict(dict) for _ in range(divide_time)]
        self.analysis = []

    def run(self, index=None):
        self.fill_relationship()
        self.calculate_relationship(index)

    def fill_relationship(self):
        for i in range(len(self.script.content)):
            if not isinstance(self.script.content[i], TIMEPLACE) and self.script.content[i].listen != set() and \
                    self.script.content[i].speak:
                speaker = self.script.content[i].speak.name
                listener = list(self.script.content[i].listen)[0].name
                if speaker == '' or listener == '':
                    continue
                polarity = self.vader.polarity_scores(self.script.content[i].modified_text)
                if not self.relationship[speaker].get(listener):  # initialize if new relationship
                    self.relationship[speaker][listener] = {'compound': 0, 'romance': 0, 'topdown': 0, 'occurance': 0,
                                                            'text': []}
                self.relationship[speaker][listener]['compound'] += polarity['compound']
                self.relationship[speaker][listener]['occurance'] += 1
                self.relationship[speaker][listener]['text'].append(self.script.content[i].modified_text)

                # Per-act relationship
                act = i * len(self.relationship_per_act) // len(self.script.content)
                if not self.relationship_per_act[act][speaker].get(listener):  # initialize if new relationship
                    self.relationship_per_act[act][speaker][listener] = {'compound': 0, 'romance': 0, 'topdown': 0,
                                                                         'occurance': 0, 'text': []}
                self.relationship_per_act[act][speaker][listener]['compound'] += polarity['compound']
                self.relationship_per_act[act][speaker][listener]['occurance'] += 1
                self.relationship_per_act[act][speaker][listener]['text'].append(self.script.content[i].modified_text)

    def calculate_relationship(self, index=None):
        self.analysis = []
        if index is None:
            relations = self.relationship
        else:
            relations = self.relationship_per_act[index]
        for speaker in relations:
            for listener in relations[speaker]:
                relationship = relations[speaker][listener]
                # determine friendliness OR hostility
                sentiment = relationship['compound'] / relationship['occurance']

                # lovingness
                lovingness = 0
                if sentiment > 0:  # and speaker.sex != listener.sex:
                    for conv in relationship['text']:
                        pos_text = nltk.pos_tag(word_tokenize(conv.lower()))
                        for love_keyword in [('love', '*'), ('like', 'V*'), ('darling', '*'), ('wife', '*'),
                                             ('husband', '*'), ('marry', '*')]:
                            for word_info in pos_text:
                                if love_keyword[0] == word_info[0]:
                                    if love_keyword[1] != "*":
                                        if not re.match(love_keyword[1], word_info[1]):
                                            continue
                                    lovingness += 1

                # topdown
                servant = 0
                for conv in relationship['text']:
                    for servant_keyword in ['your majesty', 'your highness']:
                        if servant_keyword in conv.lower():
                            servant += 1

                # print(f"Speaker: {speaker}, Listener: {listener}, sentiment: {sentiment}, lovingness: {lovingness}, servant: {servant}")
                self.analysis.append({
                    'speaker': speaker,
                    'listener': listener,
                    'sentiment': sentiment,
                    'lovingness': lovingness,
                    'servant': servant
                })
                # save scores
                relationship['result_compound'] = sentiment
                relationship['result_romance'] = lovingness
                relationship['result_topdown'] = servant

    def analyze_personality(self):
        pos = [relationship['sentiment'] for relationship in self.analysis if relationship['sentiment'] > 0]
        neg = [relationship['sentiment'] for relationship in self.analysis if relationship['sentiment'] < 0]
        mean_pos = sum(pos) / len(pos)
        mean_neg = sum(neg) / len(neg)
        lovingness = {'speaker': [0, 0, 0, 0, 0],
                      'listener': [0, 0, 0, 0, 0],
                      'count': 0}
        servant = {'speaker': [0, 0, 0, 0, 0],
                   'listener': [0, 0, 0, 0, 0],
                   'count': 0}
        affinity = {'speaker': [0, 0, 0, 0, 0],
                    'listener': [0, 0, 0, 0, 0],
                    'count': 0}
        hostile = {'speaker': [0, 0, 0, 0, 0],
                   'listener': [0, 0, 0, 0, 0],
                   'count': 0}

        for relationship in self.analysis:
            speaker = script.get_character_by_name(relationship['speaker'])
            listener = script.get_character_by_name(relationship['listener'])

            if relationship['lovingness'] > 0:
                lovingness['speaker'] = [sum(x) for x in zip(lovingness['speaker'], speaker.get_PERSONALITY())]
                lovingness['listener'] = [sum(x) for x in zip(lovingness['listener'], listener.get_PERSONALITY())]
                lovingness['count'] += 1

            if relationship['servant'] > 0:
                servant['speaker'] = [sum(x) for x in zip(servant['speaker'], speaker.get_PERSONALITY())]
                servant['listener'] = [sum(x) for x in zip(servant['listener'], listener.get_PERSONALITY())]
                servant['count'] += 1

            if relationship['sentiment'] > mean_pos:
                affinity['speaker'] = [sum(x) for x in zip(affinity['speaker'], speaker.get_PERSONALITY())]
                affinity['listener'] = [sum(x) for x in zip(affinity['listener'], listener.get_PERSONALITY())]
                affinity['count'] += 1

            if relationship['sentiment'] < mean_neg:
                hostile['speaker'] = [sum(x) for x in zip(hostile['speaker'], speaker.get_PERSONALITY())]
                hostile['listener'] = [sum(x) for x in zip(hostile['listener'], listener.get_PERSONALITY())]
                hostile['count'] += 1

        if lovingness['count'] > 0:
            lovingness['speaker'] = [x / lovingness['count'] for x in lovingness['speaker']]
            lovingness['listener'] = [x / lovingness['count'] for x in lovingness['listener']]

        if servant['count'] > 0:
            servant['speaker'] = [x / servant['count'] for x in servant['speaker']]
            servant['listener'] = [x / servant['count'] for x in servant['listener']]

        if affinity['count'] > 0:
            affinity['speaker'] = [x / affinity['count'] for x in affinity['speaker']]
            affinity['listener'] = [x / affinity['count'] for x in affinity['listener']]

        if hostile['count'] > 0:
            hostile['speaker'] = [x / hostile['count'] for x in hostile['speaker']]
            hostile['listener'] = [x / hostile['count'] for x in hostile['listener']]

        print('lovingness: ', lovingness)
        print('servant: ', servant)
        print('affinity: ', affinity)
        print('hostility: ', hostile)


def run_relationship():
    relationship_analyzer = Analyzer()
    relationship_analyzer.run()


def build_graph(analyzer, savefile='relationship.png'):
    graph = nx.MultiDiGraph()
    for analysis in analyzer.analysis:
        if not analysis['sentiment'] and not analysis['lovingness'] and not analysis['servant']:
            continue

        graph.add_node(analysis['speaker'], node_size=1000)
        graph.add_node(analysis['listener'], node_size=1000)

        if analysis['servant'] > 0:
            graph.add_edge(analysis['listener'], analysis['speaker'], color='green', penwidth=analysis['servant'])

        if analysis['lovingness'] > 0:
            graph.add_edge(analysis['speaker'], analysis['listener'], color='pink', penwidth=analysis['lovingness'] / 2)
        else:
            if analysis['sentiment'] > 0:
                graph.add_edge(analysis['speaker'], analysis['listener'], color='blue',
                               penwidth=analysis['sentiment'] * 20)
            else:
                graph.add_edge(analysis['speaker'], analysis['listener'], color='red',
                               penwidth=-analysis['sentiment'] * 20)

    agraph = nx.nx_agraph.to_agraph(graph)
    agraph.draw(savefile, prog='circo')


if __name__ == '__main__':
    # run_relationship()
    with open('./bin/script_characteristic.pickle', 'rb') as f:
        script = pickle.load(f)

    analyzer = Analyzer(script)
    analyzer.fill_relationship()

    analyzer.calculate_relationship(0)
    analyzer.analyze_personality()
    build_graph(analyzer, 'graph_act1.png')

    analyzer.calculate_relationship(1)
    analyzer.analyze_personality()
    build_graph(analyzer, 'graph_act2.png')

    analyzer.calculate_relationship(2)
    analyzer.analyze_personality()
    build_graph(analyzer, 'graph_act3.png')
