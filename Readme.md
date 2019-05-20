Name
====

直腸肛門奇形研究会が推奨する臨床的排便機能評価スコアを、自作マークシートを使って、臨床情報を集計しデータ化するシステムを開発しました。

## Description

## Demo

## VS. 

## Requirement
* macOS
* Python 2.7+

### Terminalからinstallする必要があるライブラリ
* OpenCV: 画像処理やパターン認識などを行う
* pdf2image: マークシートをスキャンしたPDFをPNGに変換する
* PyPDF2: 複数のPDFファイルを連結して1つにする

```bash
# OpenCV
pip install opencv-python

# pdf2image
pip install pdf2image --user

# PyPDF2
pip install pypdf2
```



## Usage
* [PythonとOpenCVで簡易OMR（マークシートリーダ）を作る](https://qiita.com/sbtseiji/items/6438ec2bf970d63817b8)
* [Python初心者がnumpyとOpenCVをインストールするためにしたこと](https://www.pediatricsurgery.site/entry/2018/12/24/130442)
* [【PythonとOpenCVで簡易OMR(マークシートリーダ)を作る】を初心者が理解するために①](https://www.pediatricsurgery.site/entry/2018/12/24/154519)
* [【PythonとOpenCVで簡易OMR(マークシートリーダ)を作る】を初心者が理解するために②
Python](https://www.pediatricsurgery.site/entry/2018/12/25/231014)
* [【PythonとOpenCVで簡易OMR(マークシートリーダ)を作る】を初心者が理解するために③](https://www.pediatricsurgery.site/entry/2018/12/29/195859)


## Install
もしPython初心者の方でつまずくことがあった場合は、下記の記事を参考にしてもらえるといいかもしれません。

[Python初心者がnumpyとOpenCVをインストールするためにしたこと](https://www.pediatricsurgery.site/entry/2018/12/24/130442)

### 1. numpyのinstall
```python
import numpy as np
```

### 2. OpenCVのinstall
```bash
pip install opencv-python
```


## Contribution

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[tcnksm](https://github.com/tcnksm)

# Acknowledgments
