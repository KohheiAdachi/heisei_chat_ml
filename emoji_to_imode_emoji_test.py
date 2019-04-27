# -*- coding:utf-8 -*-


import text_to_pkebell as pkebell
import json
import csv


emoji_json_file = open("../emoji-ja/data/emoji_ja.json","r")
emoji_json = json.load(emoji_json_file)

def write_csv(emoji,word):
    write_ele = [emoji,word]
    with open("result_imode_emoji_to_emoji.txt",mode="a",encoding='utf-8') as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerow(write_ele)

for emoji in emoji_json:
    word = pkebell.emoji_to_imode_emoji(emoji)
    write_csv(emoji,word)

