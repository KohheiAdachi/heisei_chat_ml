# -*- coding:utf-8 -*-

from gensim.models import KeyedVectors
import MeCab
import json
import os
from glob import glob

model_dir = "entity_vector.model.bin"

model = KeyedVectors.load_word2vec_format(model_dir,binary=True)

# emojiのjsonファイルの読み込み
emoji_json_file = open("../emoji-ja/data/emoji_ja.json","r")
emoji_json = json.load(emoji_json_file)

# imode_emojiの読み込み
imode_emoji_path = glob("../emoji_to_imode_emoji/imode_emoji_data/*")


# TODO:ベクトルを取得時にない単語に対してエラーが出る

emoji = "😘"

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

    # simi_vector = model.most_similar(emoji_keywords_list)


