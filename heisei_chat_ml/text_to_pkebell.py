# -*- coding:utf-8 -*-

from gensim.models import KeyedVectors
import MeCab
import numpy as np
import re
import json
import os
from glob import glob
import emoji
from .const import pkebell_dic

# モデルの読み込み
model_dir = "entity_vector.model.bin"
model = KeyedVectors.load_word2vec_format(model_dir, binary=True)

# emojiの読み込み
emoji_dir = os.path.dirname(__file__) + "/../emoji-ja/data/emoji_ja.json"
emoji_json_file = open(emoji_dir, "r")
emoji_json = json.load(emoji_json_file)

# imode_emojiの読み込み
imode_emoji_paths = glob("imode_emoji_data/*")

imode_emoji_lists = []
# ファイルパスから名前だけのリストを作成する
for imode_emoji_file_path in imode_emoji_paths:
    imode_emoji_lists.append(os.path.splitext(os.path.basename(imode_emoji_file_path))[0])

remove_lists = ["モバＱ", "fax to", "iモード（枠付き）", "iモード", "がく～（落胆した顔）"]
# リストから削除
for remove_name in remove_lists:
    imode_emoji_lists.remove(remove_name)


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
        if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞' or fields[0] == '副詞' or fields[0] == '感動詞':
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


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def sim_word_pkebell(word):
    max_sim = 0
    max_sim_word = ""
    v1 = get_vector_using_model(word)
    for text in pkebell_dic:
        try:
            v2 = get_vector_using_model(text)
            sim = cos_sim(v1, v2)
        except:
            sim = 0
        if max_sim < sim:
            max_sim = sim
            max_sim_word = text
    return max_sim, max_sim_word, pkebell_dic[max_sim_word]


def text_to_pkebell(text, threshold=0.5):
    sentense = re.findall(r'[^。]+(?:[。]|$)', text)
    pkebell_words = []
    pkebell_numbers = []
    for se in sentense:
        words_list = tokenize(se)
        for word in words_list:
            try:
                similarity, pkebell_word, pkebell_number = sim_word_pkebell(word)
                if similarity > threshold:
                    pkebell_words.append(pkebell_word)
                    pkebell_numbers.append(pkebell_number)
            except:
                pass

    return pkebell_words, pkebell_numbers


def emoji_to_vector(word_list, word_i=0):
    if word_i > 10:
        return np.zeros(200)
    try:
        vector = model.wv[word_list[word_i]]
    except:
        word_i = word_i + 1
        vector = emoji_to_vector(word_list, word_i)
    return vector


# TODO:エラー時に，一時形態素解析を加える
def imode_emoji_to_vector(text):
    # imode_emoji_vector = imode_emoji_to_vector2(tokenize(text)) 
    try:
        imode_emoji_vector = model.wv[text]
    except:
        imode_emoji_vector = imode_emoji_to_vector2(tokenize(text)[0])
    return imode_emoji_vector


# iモード絵文字からベクトル２回目
def imode_emoji_to_vector2(text):
    try:
        imode_emoji_vector = model.wv[text]
    except:
        imode_emoji_vector = np.zeros(200)
    return imode_emoji_vector


def emoji_to_text_lists(emoji):
    text_lists = emoji_json[emoji]["keywords"]
    return text_lists


def emoji_to_imode_emoji(emoji):
    max_simi_rate = 0
    max_simi_word = ""
    emoji_vector = emoji_to_vector(emoji_to_text_lists(emoji))

    for imode_emoji_name in imode_emoji_lists:
        # print(imode_emoji_name)
        imode_emoji_vector = imode_emoji_to_vector(imode_emoji_name)
        simi_rate = cos_sim(emoji_vector, imode_emoji_vector)
        if max_simi_rate < simi_rate:
            max_simi_rate = simi_rate
            max_simi_word = imode_emoji_name

    return max_simi_word + ".png"


def emoji_text_to_imode_text(text):
    for c in text:
        if c in emoji.UNICODE_EMOJI:
            imode_text = emoji_to_imode_emoji(c)
            text = text.replace(c, "[" + imode_text + "]")

    return text


def text_to_dic(text):
    ret_text = ""
    ret_text = ""
    id_num = 0
    textlist = []
    for c in text:
        if c in emoji.UNICODE_EMOJI:
            # text = text.replace(c,"hoge")
            # textlist.append(ret_text)
            # textlist.append(c)
            if ret_text != "":
                text_dic = {}
                text_dic["id"] = id_num
                text_dic["text"] = ret_text
                id_num += 1
                textlist.append(text_dic)
            text_dic = {}
            text_dic["id"] = id_num
            text_dic["emoji"] = emoji_to_imode_emoji(c)
            id_num += 1
            textlist.append(text_dic)
            ret_text = ""
        else:
            ret_text += c
    if ret_text != "":
        text_dic = {}
        text_dic["id"] = id_num
        text_dic["text"] = ret_text
        textlist.append(text_dic)
        id_num += 1
    return textlist


def get_emoji_to_imode_emoji():
    emoji_lists = []
    imode_emoji_lists = []
    for emoji_str in emoji_json:
        imode_emoji_name = emoji_to_imode_emoji(emoji_str)
        emoji_lists.append(emoji_str)
        imode_emoji_lists.append(imode_emoji_name)

    return emoji_lists, imode_emoji_lists
