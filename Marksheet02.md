# 0. はじめに

[https://qiita.com/sbtseiji/items/6438ec2bf970d63817b8:embed:cite]

この記事は[@sbtseiji](https://qiita.com/sbtseiji)さんがQiitaに投稿した記事をPython初心者が、その仕組みを理解して実行できるようになるために一歩一歩進んでいくための記事です。上級者はおそらく元記事を見れば理解できると思いますが、素人にはなかなか難しいのでGoogle先生に教えてもらいながら少しずつ歩みを進めていきます。前回の記事で、PythonとOpenCVとNumpyをインストールするまでの悪戦苦闘を記事にしました。

[https://www.pediatricsurgery.site/entry/2018/12/24/130442:embed:cite]

# 1. 回答のpngファイルを読み込む
```python
import cv2
Answer = cv2.imread('PNG/Answer2.png', 0)
```

# 2. 切り出した画像のリサイズ
* この後にマーク部分の画像を等間隔で切り出すという作業を行う
* 処理をしやすくするため、マークの列数・行数の整数倍のサイズになるようリサイズする
* 行数はマーカーまでの余白も考慮した行数にするのが大事

```python
n_col = 7 # マークの列数
n_row = 7 # マークの行数
margin_top = 3 # 上余白行数
margin_bottom = 1 # 下余白行数

n_row_total = n_row + margin_top + margin_bottom # 行数 (マーク行 7行 + 上余白 3行 + 下余白 1行)

Answer_Resize = cv2.resize(Answer, (n_col*100, n_row_total*100))
cv2.imwrite('PNG/Answer_Resize.png', Answer_Resize)
```
こんな形の画像に変形されていることがわかります。実際に画像サイズを確認してみましょう。

```python
>>> print(Answer.shape)
(477, 154)
>>> print(Answer_Resize.shape)
(1100, 700)
```
縦のサイズはマークの行数7に上下の余白4を足した11の100倍になっていることがわかります。

# 3. 画像処理を行う
さらに，切り出した画像に対して軽くブラーをかけた上で画像を白黒2値化し，白黒を反転させます。下の例では，Gaussianブラーをかけた上で，明るさ50を基準に2値化しています。白黒の反転は，画像値を255から引くだけです。

# 3. ブラーをかける
まずブラーをかけます。ブラーとはぼかしのことです。[OpenCVのチュートリアル](http://lang.sist.chukyo-u.ac.jp/classes/OpenCV/py_tutorials/py_imgproc/py_filtering/py_filtering.html)によると

> 画像のぼかしは、ローパスフィルタのカーネルを重畳積分することで実現でき、画像中のノイズ除去などに使う。画像中の高周波成分(エッジやノイズ)を消すことで、結果として画像全体がぼける。

https://lp-tech.net/articles/KMHfN

## ローパスフィルタとは？
とあります。ローパスフィルタとは、低周波数のみを通すようなフィルタのことのようです。画像で周波数？というのが不思議に思ったのですが、上記のサイトによると、

> 1ピクセル動いたときに、どのくらい画素が変化するかによって周波数を考えることができるのです。画素値の変化が大きいところは周波数大で画素値の変化が小さいところは周波数小です。

ということです。つまり例えば背景は周囲のピクセルとの変化が小さいので周波数小ですね。

## カーネルとは？
http://www.kaede-software.com/2007/12/post_476.html

によると

> 係数行列を使って畳み込み処理をすれば、画像をぼやけさせたりシャープにしたり、エッジ抽出が出来たりする。この係数行列をカーネルと言うらしい。

係数行列とか畳み込み処理のことはこのサイトに詳しくまとまっていました。線形代数ほんとに苦手…またまとめて勉強しよう。
https://www.clg.niigata-u.ac.jp/~medimg/practice_medical_imaging/imgproc_scion/4filter/index.htm

https://www.yukisako.xyz/entry/tatamikomi

## cv2.GaussianBlur
元記事ではガウシアンフィルタを採用しています。ガウシアンフィルタにはガウス関数を用いますが、で正規分布がガウス関数の1つであることを考えるとイメージがつきやすいかもしれません。

* 箱型フィルタがカーネル内のフィルタ係数が一様だった
  * ガウシアンフィルタは注目画素との距離に応じて重みを変えるガウシアンカーネルを採用する
* ガウシアンフィルタは白色雑音の除去に適している
* カーネルの縦幅と横幅 ( どちらも奇数 ) を指定する
* ガウシアンの標準偏差値sigmaX ( 横方向 ) とsigmaY ( 縦方向 ) を指定する必要がある
* sigmaXしか指定されなければ、sigmaYはsigmaXと同じとみなされる
* どちらの値も0にした場合、カーネルのサイズから自動的に計算される

つまりこういうことになります。

```python
cv2.GaussianBlur(Image, (kernelX,kernelY), sigmaX)
```

```python
Answer_Blur = cv2.GaussianBlur(Answer_Resize, (5,5), 0)
cv2.imwrite('PNG/Answer_Blur.png',Answer_Blur)
```

## せっかくなのでいろいろ条件を変えてみる
### カーネルのサイズを大きくする
```python
Answer_Blur2 = cv2.GaussianBlur(Answer_Resize, (25,25), 0)
cv2.imwrite('PNG/Answer_Blur2.png',Answer_Blur2)
```
ぼかしが強くなります。

### ガウシアンの標準偏差値を大きくする
```python
Answer_Blur3 = cv2.GaussianBlur(Answer_Resize, (5,5), 10)
cv2.imwrite('PNG/Answer_Blur3.png',Answer_Blur3)
```
ぼかしがほんの少し強くなった気もしますが…よくわかりません。



# 4. 2値化処理
2値化処理に関しては、[この記事](http://ipr20.cs.ehime-u.ac.jp/column/gazo_syori/chapter4.html)が非常に参考になりました。2値化処理とは

> 白黒画像といっても、白や黒だけでなくうすーい灰色や、濃いー灰色を使って表現しています。ここで、ある適当な2つの濃度値に濃度変換する処理のことを『2値化処理』といいます。画像を2値化するメリットとしては、対象とする画像と背景画像を切り離すという処理を簡単に行えるという点です。2値化は文字などを背景から引き離すときなどに有効です。

ということのようです。この際の手法としては

> 2値化処理とは、ある濃度値より小さいものは濃度値をいくらに変更し、ある濃度値より大きいものは濃度値をいくらに変更するよ、といった濃度変換処理をします。ここで濃度変換の分かれ目となる濃度値を、しきい値といいます。このしきい値の設定をかえるだけで、簡単にいろんな画像を得ることができます。

しきい値って漢字で書くと閾値って書くんですね。で、上記のサイトの閾値による2値化は、いろいろな手法があるうちの、"単純な閾値処置"に該当するようです。50を閾値として2値化するには、



```python
RetVal, Answer_Binarization = cv2.threshold(Answer_Blur, 50, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
```

と書けばよいようです。

## cv2.thereshold
[OpenCVのチュートリアル](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html)によると、ここで使われている`cv2.thereshold`は

* 第1引数: 入力画像
  * グレースケール画像でなければいけない
* 第2引数: しきい値
  * 画素値を識別するために使われる
* 第3引数: 最大値でしきい値以上の値を持つ画素に対して割り当てられる値
* 第4引数: しきい値処理の種類
  * `cv2.THRESH_BINARY`
  * `cv2.THRESH_BINARY_INV`
  * `cv2.THRESH_TRUNC`
  * `cv2.THRESH_TOZERO`
  * `cv2.THRESH_TOZERO_INV`

というように使用します。ちなみに`cv2.threshold`は二つの出力を返します。一つ目の出力は`retval`であり、大津の二値化というものに使うようです。第4引数に指定している`cv2.THRESH_OTSU`に関係しているようなのですが、今回の処理には直接関係ないため、[OpenCVのチュートリアル](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html)を読んでください。

二つ目の出力がしきい値処理された後の二値画像になり、こっちを使っていきます。


## ところで255の意味は？
確かに色を数字で表現することってしばしば見るのですが、あまり深く考えたことはありませんでした。RGBカラーモデルというものを理解すれば良いようです。[Wikipedia](https://ja.wikipedia.org/wiki/RGB)によると、

> RGBカラーモデルにおける色は、赤・緑・青の各要素がどれだけ含まれているかで記述することができる。各要素は輝度最小（闇）から輝度最大までの範囲を持つ。もし各要素とも最小なら、表示結果は黒になる。もし各要素とも最大なら、表示結果は白になる。

> 色の明度は0から255までの256個の数字でも表現できる。これはコンピュータにおける色の表示によく使われているが、プログラマが各要素の明度を8ビット（1バイト）以内の数字で表すのに便利なためである。

つまり

* (0, 0, 0) は黒
* (255, 255, 255) は白
* (255, 0, 0) は赤
* (0, 255, 0) は緑
* (0, 0, 255) は青

で表現されることになるということになります。ああ、目から鱗でした。

## 画像を確認してみる
```python
cv2.imwrite('PNG/Answer_Binarization.png',Answer_Binarization)
```
確かに、白か黒かの画像になっていますね。ちょっと感動しました

# 5. 白黒反転
255という数字についてちょっと勉強しておいたおかげで、このスクリプトの意味がよくわかりました。0(黒)が255(白)になりますよね。ああ面白い。

```python
Answer_Reverse = 255 - Answer_Binarization

cv2.imwrite('PNG/Answer_Reverse.png',Answer_Reverse)
```
できあがった画像をみてみると、確かに白黒反転されています。

# 6. マークの認識
マークの認識は，切り出してリサイズした画像を，さらに行ごとに切り分けて行います。

行ごとに行う処理としては，まず画像を横方向にマークの個数分に分割し，それぞれの画像値の合計を求めます。画像は白黒反転させていますので，色のついている部分が白(255)，空白部分が黒(0)になっています。つまり画像値の合計は，色がついている部分（マークされている部分）の面積を意味することになります。

そしてマークされている部分の面積の 中央値 を算出し，この中央値をマークされているかどうかを判断する際の 閾値 として用います。マークシートには，印刷されている線や数字など，元々色のついている部分がありますので，マークされていない部分にもある程度色がついています。そこで次の例では，色のついている部分の面積が算出した中央値の3倍以上ある場合をTrue，そうでない場合をFalseとして判断しています。この倍数は，必要に応じて調整してください。倍数を大きくするほど判定が厳しく，小さくするほど甘くなります。

なおこの方法は，各行で塗りつぶされるマークは１個または２個程度ということを前提にしています。中央値を基準にしていますので，すべてのマークが塗りつぶされていたりするとうまく動作しません。

```python
### 結果を入れる配列を用意
result = []

### 行ごとの処理(余白行を除いて処理を行う)
for row in range(margin_top, n_row - margin_bottom):

    ### 処理する行だけ切り出す
    tmp_img = img [row*100:(row+1)*100,]
    area_sum = [] # 合計値を入れる配列

    ### 各マークの処理
    for col in range(n_col):

        ### NumPyで各マーク領域の画像の合計値を求める
        area_sum.append(np.sum(tmp_img[:,col*100:(col+1)*100]))

    ### 画像領域の合計値が，中央値の3倍以上かどうかで判断
    result.append(area_sum > np.median(area_sum) * 3)
```

