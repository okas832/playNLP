from defs import *
from tqdm import tqdm
import re
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.lm import Vocabulary
from nltk.classify.naivebayes import NaiveBayesClassifier as NB

# class MBTI
#   MBTI data
class MBTI():
    def __init__(self):
        self.M = 0
        self.B = 0
        self.T = 0
        self.I = 0

    # get_MBTI
    # return MBTI value in tuple format
    def get_MBTI(self):
        return (self.M, self.B, self.T, self.I)

class CHARACTERISTIC_TRAINER():
    def __init__(self):
        self.train = {}
        self.test = {}
        self.classifier = {}
        self.vocab = Vocabulary(unk_cutoff=1)
        self.prepare_dataset(mode='train')
        self.prepare_dataset(mode="test")
        self.vocab_words = {w: 0 for w in self.vocab.counts.keys() if w in self.vocab}
        self.vocab_words['UNK'] = 0 # initially add UNK feature section
        # vocab size is currently 20124
        """uncomment this and erase the below line for full training. Currently training only gender for speed issue
        for mode in ['gender', 'age_group', 'extroverted', 'stable', 'agreeable', 'conscientious', 'openness']:
            self.run_train(mode)
        """
        self.run_train('gender')

    def prepare_dataset(self, mode="train"): # mode = ["train", "test"]
        """
        Each line of the truth files encodes the following information:
        userid:::gender:::age_group:::extroverted:::stable:::agreeable:::conscientious:::openness
        """
        print(f"prepare_dataset: {mode} START")
        if mode == "train":
            dir_path = CHAR_TRAIN_DIR
            saved = self.train
        elif mode == "test":
            dir_path = CHAR_TEST_DIR
            saved = self.test
        else:
            raise Exception("Directory name should be one of 'train' or 'test'")

        with open(dir_path+"truth.txt", "r") as f:
            truths = f.read().split('\n')[:-1]
        for truth in truths:
            userid, gender, age_group, extroverted, stable, agreeable, conscientious, openness = truth.split(":::")
            root = ET.parse(f"{dir_path}{userid}.xml").getroot()
            words = [self.preprocess_text(child.text, mode=mode) for child in root]
            saved[userid] = {"gender": gender, "age_group": age_group,
                             "extroverted": extroverted, "stable": stable,
                             "agreeable": agreeable, "conscientious": conscientious,
                             "openness": openness, "text": words}

        print(f"prepare_dataset: {mode} DONE")
    def preprocess_text(self, text, mode='train'): # clean up and tokenize text
        processed_text = []
        #remove url
        #change @username to you
        if 'http' in text:
            text = text[:text.index('http')]
        text = re.sub(r"[^A-Z a-z?!-]+", '', text)
        words = [w.lower() for w in word_tokenize(text)]
        if mode == 'train':
            self.vocab.update(words) # add corresponding word to vocab
        return words

    def get_feature_dict(self, words):
        feature_dict = self.vocab_words.copy()
        for word in words:
            if word in self.vocab:
                feature_dict[word] += 1
            else:
                feature_dict['UNK'] += 1
        return feature_dict

    def run_train(self, mode='agreeable'):
        # mode in ['gender', 'age_group', 'extroverted', 'stable',
        # 'agreeable',·'conscientious', 'openness']
        train_input = []
        print(f"making train_input: {mode}")
        for infos in tqdm(self.train.values()):
            for info in infos['text']: # process same label for 100 texts
                train_input.append((self.get_feature_dict(info), infos[mode]))
        print(f"running trainer... {mode}")
        self.classifier[mode] = NB.train(train_input)
        print("running trainer done")

    def predict(self, text, mode='gender'): # mode has to be one of classifier.keys()
        preprocessed_words = self.preprocess_text(text, mode='predict')
        feature_dict = self.get_feature_dict(preprocessed_words)
        classified = self.classifier[mode].classify(feature_dict)
        print(f"Predicted output: {classified}")

# class CHARACTER
#   data of character
#
# inheritance MBTI
#
# name - str
#   character's name
# sex - str
#   character's gender
class CHARACTER(MBTI):
    def __init__(self, name, sex):
        super().__init__()
        self.name = name
        self.sex = sex
if __name__ == "__main__":
    trainer = CHARACTERISTIC_TRAINER()
    trainer.predict('I am so hungry !', mode='gender')

