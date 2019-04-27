## テキストからポケベルの番号に変換する

### requirement

#### ライブラリ関係

- gensim
- Mecab

### 学習済みモデル

このリンク	<http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/>の20170201.tar.bz2(1.3GB,解凍後2.6GB)を使用するのでダウンロードして下さい．

### 使い方

```python
import text_to_pkebell as pkebell

# 類似後のThresholdの初期値は0.5
word_lists,word_number = pkebell.text_to_pkebell("渋谷に集合ね",threshold=0.5)

print(word_lists)
# ['渋谷', '集合']
print(word_number)
# ['428', '4951']
```

みたいな感じ．．．．

### エラー処理関係

単語は，動詞，名詞，副詞，感動詞に限定

モデルに存在しない単語は，無視することにしました．

例えば”ハッカソン”という単語はなかったです．辛い．

## emojiからIモードの絵文字に変換する

### requirement

#### ライブラリ関係

ポケベル時と一緒だと思う

#### 学習済みモデル

ポケベル時と同様

#### emoji絵文字の辞書

<https://github.com/yagays/emoji-ja>

これをクローンして下さい．

#### iモード絵文字

https://drive.google.com/open?id=1M9Mkcp33UopanwE1VHAwSzRnNiimeFl6

ここからダウンロードして下さい

### パス設定

```python
# emojiの読み込み
emoji_dir = "emoji_ja.jsonのパス"
emoji_json_file = open(emoji_dir,"r")
emoji_json = json.load(emoji_json_file)

# imode_emojiの読み込み
imode_emoji_paths = glob("iモード絵文字が入っているフォルダのパス/*")

```

### その他

```def emoji_to_vector
def emoji_to_vector
```

で再帰使ってるので，大丈夫だと思うけど， ~~もし落ちたらごめん~~

testで検証してるので，多分落ちない

### 使い方

```python
import text_to_pkebell as pkebell

imode_emoji = pkebell.emoji_to_imode_emoji("😽")
print(imode_emoji)
# 猫
```

iモード絵文字の画像ファイル名は

`imode_emoji + ".png"`になってます．