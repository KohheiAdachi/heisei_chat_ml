# -*- coding:utf-8 -*-

from gensim.models import KeyedVectors
import MeCab
import numpy as np
import re
from const import pkebell_dic
import json
import os
from glob import glob

# モデルの読み込み
model_dir = "entity_vector.model.bin"
model = KeyedVectors.load_word2vec_format(model_dir,binary=True)

# emojiの読み込み
emoji_dir = "../emoji-ja/data/emoji_ja.json"
emoji_json_file = open(emoji_dir,"r")
emoji_json = json.load(emoji_json_file)

# imode_emojiの読み込み
imode_emoji_path = glob("../emoji_to_imode_emoji/imode_emoji_data/*")


def tokenize(doc):
    mecab = MeCab.Tagger("-Ochasen")
    lines = mecab.parse(doc).splitlines()
    words = []
    stop_words = []
    for line in lines:
        chunks = line.split('\t')
        if len(chunks) > 3 and not chunks[2] in stop_words:
            if chunks[3].startswith('動詞'):
                words.append(chunks[2])
            if chunks[3].startswith('名詞') and not chunks[0] in stop_words:
                words.append(chunks[0])
            if chunks[3].startswith('副詞'):
                words.append(chunks[0])
            if chunks[3].startswith('感動詞'):
                words.append(chunks[0])
#             if chunks[3].startswith('形容詞'):
#                 words.append(chunks[2])
#             if chunks[3].startswith('形容動詞'):
#                 words.append(chunks[2])    
    return words

def get_vector(text):
    mt = MeCab.Tagger('')
    mt.parse('')
    sum_vec = np.zeros(200)
    word_count = 0
    node = mt.parseToNode(text)
    while node:
        fields = node.feature.split(",")
        # 名詞、動詞、形容詞、副詞、感動詞に限定
        if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞'or fields[0] == '副詞' or fields[0] == '感動詞':
            sum_vec += model.wv[node.surface]
            word_count += 1
        node = node.next
    
    return sum_vec / word_count

def get_vector_using_model(word):
    try:
        vector = model[word]
    except:
        vector = np.zeros(200)
    return vector

def cos_sim(v1,v2):
    return np.dot(v1,v2)/(np.linalg.norm(v1) * np.linalg.norm(v2))

def sim_word_pkebell(word):
    max_sim = 0
    max_sim_word = ""
    v1 = get_vector_using_model(word)
    for text in pkebell_dic:
        try:
            v2 = get_vector_using_model(text)
            sim = cos_sim(v1,v2)
        except:
            sim = 0
        if max_sim < sim:
            max_sim = sim
            max_sim_word = text
    return max_sim,max_sim_word,pkebell_dic[max_sim_word]


def text_to_pkebell(text,threshold=0.5):
    sentense = re.findall(r'[^。]+(?:[。]|$)',text)
    pkebell_words = []
    pkebell_numbers = []
    for se in sentense:
        words_list = tokenize(se)
        for word in words_list:
            try:
                similarity,pkebell_word,pkebell_number = sim_word_pkebell(word)
                if similarity > threshold:
                    pkebell_words.append(pkebell_word)
                    pkebell_numbers.append(pkebell_number)
            except:
                pass
                
    return pkebell_words,pkebell_numbers

def emoji_to_imode_emoji(emoji):
    max_simi_rate = 0
    max_simi_word = ""
    emoji = emoji_json[emoji]["keywords"]
    emoji_vecter = model.most_similar(emoji[0])
    print(emoji_vecter)
    for imode_emoji in imode_emoji_path:
        print(imode_emoji)
        imode_emoji_text = os.path.splitext(os.path.basename(imode_emoji))
        print(emoji[0],imode_emoji)
        simi = model.similarity(emoji[0],imode_emoji_text[0])
        print(simi)
        if simi > max_simi_rate:
            max_simi_rate = simi
            max_simi_word = imode_emoji_text[0]
    return max_simi_rate,max_simi_word
        
    # emoji_list = []
    # try:
    #     simi_vector = model.most_similar(emoji_list)
    # except:
    #     emoji_list.pop(-1)
