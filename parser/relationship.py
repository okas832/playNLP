from nltk.sentiment.vader import SentimentIntensityAnalyzer
from script import TIMEPLACE
from collections import defaultdict
from nltk.tokenize import word_tokenize
import nltk
import re


"""
class Analyzer: calculate sentiment, lovingness, and servant relationship scores between characters.
to use, please call analyzer at the end of anaphora_resolution.py.
and run: python3 anaphora_resolution.py

"""
class Analyzer():
    def __init__(self, script):
        self.vader = SentimentIntensityAnalyzer()
        self.script = script
        self.relationship = defaultdict(dict)

    def run(self):
        self.fill_relationship()
        self.calculate_relationship()

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

    def calculate_relationship(self):
        for speaker in self.relationship:
            for listener in self.relationship[speaker]:
                relationship = self.relationship[speaker][listener]
                # determine friendliness OR hostility
                sentiment = relationship['compound'] / relationship['occurance']

                # lovingness
                lovingness = 0
                if sentiment > 0: # and (speaker.sex != listener.sex):
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

                print(f"Speaker: {speaker}, Listener: {listener}, sentiment: {sentiment}, lovingness: {lovingness}, servant: {servant}")
                # save scores
                relationship['result_compound'] = sentiment
                relationship['result_romance'] = lovingness
                relationship['result_topdown'] = servant



def run_relationship():
    relationship_analyzer = Analyzer()
    relationship_analyzer.run()



if __name__ == '__main__':
    run_relationship()
