# Pythonのversionを確認する
```
$ python --version
Python 2.7.10
```
どうやらPython2がインストールされているらしい。

# Python2とPython3どっちを使うか
https://hajipro.com/python/python2-python3
> これから、新しくPythonを学んでいきたい初心者はPython3系を学習していきましょう。当初は、Python2系でなければ、使えないライブラリも多々ありました。現在では、Python2系から3系への周辺のライブラリの移行もすすみ、Python3でも全く問題ありません。Python2系のサポートは2020年で終了する予定になっています。

とあるので、Python3にアップグレードします。

# Python3をインストールする
MacにPython3をインストールし環境構築【決定版】
https://qiita.com/7110/items/1aa5968022373e99ae28

## Homebrew経由でPython3をインストールする
```
$brew install python3
```
を実行すると
```
Error: The following formula
  python
cannot be installed as binary package and must be built from source.
Install the Command Line Tools:
  xcode-select --install
```
と怒られてしまう。どうやらxcodeが上手く働いていないことが問題のようなので、おとなしく従ってみる。

## Xcodeをインストールし直す
```
xcode-select --install
```
そのあとに再度

* このサイトでは`virtualenv`や`pyenv`で環境を分ける方法が推奨されているがとりあえず無視してみる


```{}
import numpy as np
import cv2
```