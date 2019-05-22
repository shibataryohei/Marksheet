# はじめに
Macユーザーの皆さんは学会でのプレゼンテーションはどうしていますでしょうか？

1つの解決策としてはWindowsとの共用フォントを使えばいいのだと思いますが、Windowsで最適とされるフォントの組み合わせがMacでうまいこと使えなかったり、そもそも宗教上の理由でヒラギノしか使えないという僕みたいな人も一定数いるのではないかと思います。

あとはPDFしちゃえばいいじゃんという声も聞こえてきそうですが、少なくとも医学系の学会ではPDFでのプレゼンテーションはみとめられていないことが多いと思います。

## フォントの埋め込み
尚、Macにしか入っていないフォントをpptファイルに埋め込んで、Windows PCで開けるようにする
という方法もあります。ここらへんは [伝わるデザイン](http://tsutawarudesign.com/yomiyasuku3.html) に詳しく記載されているのですが
、残念ながら

> 実はWindows版のPowerPointにはファイルに「フォントを埋め込む」という機能があります。この機能を使えば、どのパソコンでも自分の好きなフォントでプレゼンすることができます。
> この方法は、Windows版のPowerPointでのみ使える方法ですのでご注意ください。

ということで、MacのPowerPointでは使えないようです。

# テキストデータを画像データに変換する
そこで実は僕はPPTファイルをPowerPointを使ってPNGファイルに出力すればいいのだと気がつきました。これだとすべてテキストデータが画像データに変換されるので、フォントに依存せず、レイアウトも崩れずWindowsのPowerPointで表示することができます。

ファイルが少し重くなりますが、動画を組み込んだスライドも問題なく動くようなある程度のスペックのものが準備されていることが多いと思うので、スライドがもたついたりということはないと思います。

しかし、この方法の最大の問題点は、PNGファイルを新しく作成したPPTファイルにペタペタ貼るという苦行が必要になってきます。スライドが数枚であればなんてことはないのですが、数十枚に及ぶと時間がかなりかかりますし、修正が入ったりすると発狂します。

# RとRstudioでどうにかする
そこで`R`と`Rstudio`の力を借りてどうにかできないものかと考えて、下記の方法を編み出しました。Rstudioはver 1.2から、`.Rmd`からPPTファイルを直接生成できるようになっています。これ、本当にありがたいことです。

https://support.rstudio.com/hc/en-us/articles/360004672913-Rendering-PowerPoint-Presentations-with-RStudio

https://qiita.com/nozma/items/bbd681490b2aaaf9ec93

大まかな流れとしては  

1. 画像がスライド全体に貼り付けられるようなTemplateのPPTファイルを作成しておく
2. PowerPointでスライドをPNGで出力する
3. Markdown記法で、スライドのPNGファイルを参照するディレクトリをRで書き出す
4. Rstudioで`.Rmd`ファイルを作成
5. YAMLヘッダーに`reference_doc:`を追加
6. 本文に3.で生成した文字列を貼り付ける
7. PPTファイルに`knit`する
  
という感じになります。

# 実際の手順
## 1. TemplateのPPTファイルを作成しておく
ふつうにRstudioでPPTファイルにknitすると、こんな感じで画像がスライドの中央に縮小されて貼り付けられます。これじゃあそのままスライドにはできません。

スライド

これを解決するにはこの記事が参考になりました。

https://stackoverflow.com/questions/55598415/r-markdown-powerpoint-slide-customization

この記事に書いてあることを簡単にまとめると

1. 新規`.pptx`を作成 (`.potx`でなくていいことに注意)
2. `スライドマスター`を開く
3. `レイアウトを挿入`
4. `プレースホルダーを挿入`して画像ファイルを選択
5. プレースホルダーをスライド全体に広げる
6. `スライドマスター`を閉じる
7. この`.pptx`を`my_template.pptx`として保存

この`my_template.pptx`を後ほどtemplateとして参照すれば、Markdownで参照した画像がスライド全体に作成されます。

## 2. PowerPointでスライドをPNGで出力する
これは普通に`ファイル`->`出力`で出力フォーマットに`.png`を選択してください。

## 3. Markdown記法で、スライドのPNGファイルを参照するディレクトリをRで書き出す
```md
![](Slide01.png)
![](Slide02.png)
![](Slide03.png)
```
などと`.Rmd`に自分で書いていってもいいのですが、絶対PATHが必要なときなど面倒くさいので、Rで吐き出してもらいます。Rのコンソールで以下のスクリプトを実行してください。

```r
library(tidyverse)

PATH <- "PNGファイルのディレクトリ"

# ファイル名の変換
# Slide1 -> Slide01 にする
setwd(PATH) 
dir() %>% 
  file.rename(., gsub("(?<![0-9])([0-9])(?![0-9])",
                      "0\\1",
                      .,
                      perl = TRUE)) 

# Markdown記法で書き出し
setwd(PATH) 
dir() %>%
  paste0("![](",PATH,"/", ., ")") %>%
  noquote %>% # patse()の結果から"を除去する
  cat(., sep="\n\n") # \nは改行を表す
```

これを実行するとRstudioのconsoleに

```
![](PNGファイルのディレクトリ/Slide01.png)

![](PNGファイルのディレクトリ/Slide02.png)

![](PNGファイルのディレクトリ/Slide03.png)

![](PNGファイルのディレクトリ/Slide04.png) ...
```

と吐き出されますので、コピーして作成した`.Rmd`に貼り付けます。実はこのスクリプトには一工夫してあって、普通にPowerPointでPNGファイルに出力すると

```
slide1.png
slide2.png
:
:
slide10.png
slide11.png
```
とファイル名が設定される。このままRで出力するとPNGファイルの順番が崩れてしまうので、ファイル名を

```
slide01.png
slide02.png
:
:
slide10.png
slide11.png
```
と変換する必要があります。これをうまいこと処理する正規表現がなかなかわからなかったのですが、StackOverflowでいい記事を見つけました。ちなみにスライド数が100を超える (3桁を超えると) これだとエラーになってしまうと思います。適宜、修正をお願いします。

https://stackoverflow.com/questions/46918943/str-replace-a1-a9-to-a01-a09-and-so-on

## 4. Rstudioで`.Rmd`ファイルを作成

## 5. YAMLヘッダーに`reference_doc:`を追加

---
output: 
  powerpoint_presentation:
    reference_doc: template.pptx
---

この`reference_doc: `という部分で、1.で作成したTemplateを参照できるようになります。

## 6. 本文に3.を貼り付ける
## 7. PPTファイルに`knit`する

これでPNGファイルがスライド全体に貼り付けられたPPTファイルが完成していると思います。少し手間
はかかりますが、一度Templateを作っておけば再利用できるのでスムーズになると思います。Macユーザーの学会発表が少しでも楽になることを祈っております。

