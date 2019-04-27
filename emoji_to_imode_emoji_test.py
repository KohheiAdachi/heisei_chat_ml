# -*- coding:utf-8 -*-


import text_to_pkebell as pkebell
import json



emoji_json_file = open("../emoji-ja/data/emoji_ja.json","r")
emoji_json = json.load(emoji_json_file)

for emoji in emoji_json:
    word = pkebell.emoji_to_imode_emoji(emoji)
    print(emoji,word)

