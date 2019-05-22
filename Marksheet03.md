```python
import numpy as np
import cv2
Answer_Reverse = cv2.imread('PNG/Answer_Reverse.png', 0)
```

# マークの認識
マークの認識は切り出してリサイズした画像を、さらに行ごとに切り分けて行っています。要点としては元記事によると

> 1. 画像を横方向にマークの個数分に分割し、それぞれの画像値の合計を求める
> 2. 画像は白黒反転させているので、マーク部が白(255)、空白が黒(0)になっている
> 3. 画像値の合計 = マーク部分の面積
> 4. マーク部分の面積がある一定の値以上であれば、マークされたとカウントする

ということになります。

```python
n_col = 7 # マークの列数
n_row = 7 # マークの行数
margin_top = 3 # 上余白行数
margin_bottom = 1 # 下余白行数

# 結果を入れる配列を用意
Result = []

# for row in range(margin_top, n_row - margin_bottom):
for row in range(margin_top+1, margin_top+1+n_row):
    tmp_Answer = Answer_Reverse [(row-1)*100:row*100,]
    cv2.imwrite("PNG/Answer_Tmp%d.png" % row, tmp_Answer)
    Area_sum = []  
    for col in range(n_col):
        Area_sum.append(np.sum(tmp_Answer[:,col*100:(col+1)*100]))
    Result.append(Area_sum > np.median(Area_sum) * 3)
```

これを実行すると

```python
>>> Result
[array([ True, False, False, False, False, False, False]), array([False,  True,  True, False, False, False, False]), array([False, False,  True, False, False, False, False]), array([False, False, False,  True, False, False, False]), array([False, False, False, False,  True, False, False]), array([False, False, False, False, False,  True, False]), array([False, False, False, False, False, False,  True])]
```

```python
Area_sum.append(np.sum(tmp_Answer[:,col*100:(col+1)*100]))
```
この部分ですが、tmp_Answerをさらに列で7分割しています。その後、7分割した画像の画像値を`np.sum`で合計していて、`append`でfor構文で回した`col=0`から`col=6`までの結果を追加していき、Area_sumに代入している形になります。`row=10`の値は

```
>>> Area_sum
[0, 0, 0, 0, 0, 0, 402135]
```
となります。7番目の画像値が大きくなっていることがわかります。この部分がマークされた部分になるわけですね。

```python
Result.append(Area_sum > np.median(Area_sum) * 3)
```
それで、7個に分割した画像値のそれぞれの値が、中央値の3倍より上であればTRUE、そうでなければFALSEと返すようにし、これをResultに代入することで、マークされたかされていないかという、カテゴリー変数に変換しています。

# 結果の出力

```python
for x in range(len(Result)):
    res = np.where(Result[x]==True)[0]+1
    if len(res)>1:
        print('Q%d: ' % (x+1) +str(res)+ ' ## Multiple ##')
    elif len(res)==1:
        print('Q%d: ' % (x+1) +str(res))
    else:
        print('Q%d: ** Unanswered **' % (x+1))
```
これを実行すると
```
Q1: [1]
Q2: [2 3] ## Multiple ##
Q3: [3]
Q4: [4]
Q5: [5]
Q6: [6]
Q7: [7]
```

となります。Q2で複数回答していないのに、複数回答してしまっていることになっています。実際の画像をみてみましょう
```python
row = 5
tmp_Answer = Answer_Reverse [(row-1)*100:row*100,]
Area_sum = []  
for col in range(n_col):
    Area_sum.append(np.sum(tmp_Answer[:,col*100:(col+1)*100]))
```

```
>>> Area_sum
[0, 698445, 765, 0, 0, 0, 0]
```
と実際にはマークしていない3番目に画像値が入ってしまっていることになります。
```python
for col in range(n_col):
    tmp_Answer_Col = tmp_Answer[:,col*100:(col+1)*100]
    cv2.imwrite("PNG/Answer_Tmp5_%d.png" % col, tmp_Answer_Col)
```

画像をみてみると、2番目のマークを(わざと)大きくしたせいで、3番目の画像にほんの少し白い部分がはみ出てしまっていることが原因となります。こうなってしまうのでは、もともとマーカーで切り出した画像の左の余白がちょっとあって、7分割したときに正確に均等に分割されていないことが原因なのです。

元記事では7分割した画像の画像値の中央値を閾値としていましたが、画像値の中央値は基本的に0です(単一回答の場合)。なので、もう少し厳しい閾値にすればエラーがなくなると思います。

```python
>>> print(tmp_Answer_Col.shape)
(100, 100)
```
1つの分割した画像の解像度は100 px ✕ 100 pxになります。なので3% ( 300 px )くらいに白い部分が混じってしまっても良いとしましょう。300 pxに白 ( 255 ) が入るとすると、画像値の合計は76500となります。これを閾値としてみましょう。

```python
Result = []


# for row in range(margin_top, n_row - margin_bottom):
for row in range(margin_top+1, margin_top+1+n_row):
    tmp_Answer = Answer_Reverse [(row-1)*100:row*100,]
    Area_sum = []  
    for col in range(n_col):
        Area_sum.append(np.sum(tmp_Answer[:,col*100:(col+1)*100]))
    Result.append(Area_sum > np.median(255*300))
  

for x in range(len(Result)):
    res = np.where(Result[x]==True)[0]+1
    if len(res)>1:
        print('Q%d: ' % (x+1) +str(res)+ ' ## Multiple ##')
    elif len(res)==1:
        print('Q%d: ' % (x+1) +str(res))
    else:
        print('Q%d: ** Unanswered **' % (x+1))
```

これを実行してあげると。

```
Q1: [1]
Q2: [2]
Q3: [3]
Q4: [4]
Q5: [5]
Q6: [6]
Q7: [7]
```

正しく読めていることがわかります。実際に自分の画像をみて微調整することは必要そうですが、これでスキャンした画像から回答データを抜き出すことはできそうです。

# 3. 回答データをデータフレームにしてcsvにして抽出する
いつもお世話になっている[Bioinformatics](https://stats.biopapyrus.jp/python/dataframe.html)のページがヒットしました。どうやらPandasというものを使うといいようです。聞いたことくらいはありますね。こちらの記事によると

https://techacademy.jp/magazine/17697

> Pandasは、Pythonを使ったデータ解析を支援するために開発されたデータ操作のための高速で、簡単に利用できるようにしたライブラリです。DataFrameやSeriesといったオブジェクトを操作することでPythonから直感的にデータ操作ができるようになっています。また、データ分析をするために便利な関数が揃っているので、ファイルの入出力や時系列データの扱いなどがしやすくなっていることが特徴です。

ということです。

## Pandasのインストール
Pythonを`Control+D`で一度終了してターミナルに戻ります。
```
pip install pandas --user
```
これでOKです。Pythonに戻って解析を進めていきます。

```python
Python
import pandas as pd

Value = []

for x in range(len(Result)):
    res = np.where(Result[x]==True)[0]+1
    Value.append(int(res))

df = pd.DataFrame({'Value': Value,
                  'Variable': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
                  'Date': '2018/12/24',
                  'ChartID': '0123456789'})
```

`pd.DataFrame`でベクトルからデータフレームを作成できるようです。`df`を実行すると

```
>>> df
      ChartID        Date  Value Variable
0  0123456789  2018/12/24      1       Q1
1  0123456789  2018/12/24      2       Q2
2  0123456789  2018/12/24      3       Q3
3  0123456789  2018/12/24      4       Q4
4  0123456789  2018/12/24      5       Q5
5  0123456789  2018/12/24      6       Q6
6  0123456789  2018/12/24      7       Q7
```
csvファイルとして保存するには
```
df.to_csv("df.csv")
```
で良いようです。あとは複数の結果をターミナルから`cat`などを使って結合していけば、Long型のデータが完成していくのではないかと思われます。


print('Q', range(1,8)) +str(res)+ ' ## Multiple ##')

print(`)
```

