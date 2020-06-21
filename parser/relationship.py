from nltk.sentiment.vader import SentimentIntensityAnalyzer
from script import TIMEPLACE
from collections import defaultdict
from nltk.tokenize import word_tokenize
import nltk
import re
import pickle
import networkx as nx
import matplotlib.pyplot as plt

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
            if not isinstance(self.script.content[i], TIMEPLACE) and self.script.content[i].listen != set() and self.script.content[i].speak:
                speaker = self.script.content[i].speak.name
                listener = list(self.script.content[i].listen)[0].name
                if speaker == '' or listener == '':
                    continue
                polarity = self.vader.polarity_scores(self.script.content[i].modified_text)
                if not self.relationship[speaker].get(listener): # initialize if new relationship
                    self.relationship[speaker][listener] = {'compound': 0, 'romance': 0, 'topdown': 0, 'occurance': 0, 'text': []}
                self.relationship[speaker][listener]['compound'] += polarity['compound']
                self.relationship[speaker][listener]['occurance'] += 1
                self.relationship[speaker][listener]['text'].append(self.script.content[i].modified_text)

                # Per-act relationship
                act = i * len(self.relationship_per_act) // len(self.script.content)
                if not self.relationship_per_act[act][speaker].get(listener): # initialize if new relationship
                    self.relationship_per_act[act][speaker][listener] = {'compound': 0, 'romance': 0, 'topdown': 0, 'occurance': 0, 'text': []}
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
                if sentiment > 0: #and speaker.sex != listener.sex:
                    for conv in relationship['text']:
                        pos_text = nltk.pos_tag(word_tokenize(conv.lower()))
                        for love_keyword in [('love', '*'), ('like', 'V*'), ('darling', '*'), ('wife', '*'), ('husband', '*'), ('marry', '*')]:
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


def run_relationship():
    relationship_analyzer = Analyzer()
    relationship_analyzer.run()


def build_graph(analyzer):
    graph = nx.MultiDiGraph()
    for analysis in analyzer.analysis:
        if not analysis['sentiment'] and not analysis['lovingness'] and not analysis['servant']:
            continue

        graph.add_node(analysis['speaker'], node_size=1000)
        graph.add_node(analysis['listener'], node_size=1000)

        if analysis['servant'] > 0:
            graph.add_edge(analysis['listener'], analysis['speaker'], color='m', weight=analysis['servant'] * 10)

        if analysis['lovingness'] > 0:
            graph.add_edge(analysis['speaker'], analysis['listener'], color='g', weight=analysis['lovingness'])
        else:
            if analysis['sentiment'] > 0:
                graph.add_edge(analysis['speaker'], analysis['listener'], color='b', weight=analysis['sentiment'] * 10)
            else:
                graph.add_edge(analysis['speaker'], analysis['listener'], color='r', weight=-analysis['sentiment'] * 10)

    edges = graph.edges()
    pos = nx.circular_layout(graph)
    colors = nx.get_edge_attributes(graph, 'color').values()
    weights = nx.get_edge_attributes(graph, 'weight').values()
    nx.draw(graph, pos, with_labels=True, edges=edges, edge_color=colors, width=list(weights), font_size=8,
            node_shape='o', node_size=1000, node_color='r', alpha=0.7)
    plt.show()


if __name__ == '__main__':
    # run_relationship()
    with open('./bin/script_characteristic.pickle', 'rb') as f:
        script = pickle.load(f)

    analyzer = Analyzer(script)
    analyzer.run(2)

    build_graph(analyzer)
