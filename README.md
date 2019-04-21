# テキストからポケベルの番号に変換する

## requirement

### ライブラリ関係

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

