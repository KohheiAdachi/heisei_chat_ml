# -*- coding:utf-8 -*-

from gensim.models import KeyedVectors
import MeCab
import json
import os
from glob import glob

model_dir = "entity_vector.model.bin"

model = KeyedVectors.load_word2vec_format(model_dir,binary=True)

emoji_json_file = open("../emoji-ja/data/emoji_ja.json","r")
emoji_json = json.load(emoji_json_file)

# TODO:ベクトルを取得時にない単語に対してエラーが出るz
for emoji in emoji_json:
    emoji_text_lists =　emoji_json[emoji]["keywords"]
    emoji_list = []
    for emoji_text in emoji_text_lists:
        emoji_list.append(emoji_text)
        try:
            simi_vector = model.most_similar(emoji_list)
        except:
            emoji_list.pop(-1)
    print(simi_vector)

    # simi_vector = model.most_similar(emoji_keywords_list)


