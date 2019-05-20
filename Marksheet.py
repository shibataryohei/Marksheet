import sys
print(sys.path)
import os
os.getcwd()

# Library
import os
import numpy as np
import cv2
import pdf2image
import pandas as pd
import PyPDF2

# Folder内のpdfのリストを取得する
PDF_Files = []
PDF_Writer = PyPDF2.PdfFileWriter()
for Filename in os.listdir('/Users/Ryohei/Git/Marksheet/PDF_Input'):
    if Filename.endswith('.pdf'):
        PDF_Files.append(Filename)
 
# 全てのpdf_filesをループで回す
for Filename in PDF_Files:
    PDF_Files_Obj = open('PDF_Input/'+Filename, 'rb')
    PDF_Reader = PyPDF2.PdfFileReader(PDF_Files_Obj)
    for Page_Number in range(PDF_Reader.numPages):
        Page_Obj = PDF_Reader.getPage(Page_Number)
        PDF_Writer.addPage(Page_Obj)
  
# 結合したPDFファイルの保存
PDF_Output = open('PDF_Output/Marksheet_Merge.pdf', 'wb')
PDF_Writer.write(PDF_Output)
PDF_Output.close()


# pdfからpngに変換する
from pdf2image import convert_from_path
Marksheet_PDFs = convert_from_path('PDF_Output/Marksheet_Merge.pdf')
i = 0
for Marksheet_PDF in Marksheet_PDFs:
    Marksheet_PDF.save('PNG_Input/Marksheet{}.png'.format(i), 'png')
    i += 1
    
# pngからpreviewでマーカーを切り出す
# `Image/Marker_ANS.png`
# `Image/Marker_ID.png`としておく

# グレースケール (mode = 0) でファイルを読み込む
Marker_ANS = cv2.imread('Image/Marker_ANS.png', 0)
Marker_ID = cv2.imread('Image/Marker_ID.png', 0)

# Folder内のpngのリストを取得する
PNG_Files = []
for Filename in os.listdir('/Users/Ryohei/Git/Marksheet/PNG_Input'):
    if Filename.endswith('.png'):
        PNG_Files.append(Filename)


Marksheet = cv2.imread('Image/Marksheet.png', 0) 

for Marksheet_PDF in Marksheet_PDFs:
# ID
# Markerに囲まれた範囲を設定する
Marker_Match = cv2.matchTemplate(Marksheet, Marker_ID, cv2.TM_CCOEFF_NORMED)
Marker_Location = np.where( Marker_Match >= 0.7 ) # 閾値を設定

# 切り出し範囲を設定
Markarea = {}
Markarea['top_x'] = min(Marker_Location[1]) # loc[1]がx軸を表す
Markarea['top_y'] = min(Marker_Location[0]) # loc[0]がx軸を表す
Markarea['bottom_x'] = max(Marker_Location[1])
Markarea['bottom_y'] = max(Marker_Location[0])

# Y軸方向のマーカーのサイズを取り出す
Marker_ID_Y = Marker_ID.shape[1]
Marker_ID_X = Marker_ID.shape[0]

# 切り出し
# こうすると余白がなくなる
ID = Marksheet[(Markarea['top_y']+Marker_ID_Y):Markarea['bottom_y'],Markarea['top_x']:Markarea['bottom_x']+Marker_ID_X]
cv2.imwrite('Image/ID.png',ID)

# Resize
n_col = 17
n_row = 10
margin_top = 4
ID_Resize = cv2.resize(ID, (n_col*100, (n_row+margin_top)*100))
cv2.imwrite('Image/ID_Resize.png', ID_Resize)

# Blur
ID_Blur = cv2.GaussianBlur(ID_Resize, (25,25), 0)
cv2.imwrite('Image/ID_Blur.png',ID_Blur)

# 2値化
RetVal, ID_Binarization = cv2.threshold(ID_Blur, 50, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite('Image/ID_Binarization.png',ID_Binarization)

# 反転
ID_Reverse = 255 - ID_Binarization
cv2.imwrite('Image/ID_Reverse.png',ID_Reverse)

# 分割
# for row in range(margin_top, n_row - margin_bottom):
Result = []
for col in range(n_col):
    tmp_ID = ID_Reverse [:,col*100:(col+1)*100]
    Area_sum = []  
    for row in range(margin_top, margin_top+n_row):
        Area_sum.append(np.sum(tmp_ID[row*100:(row+1)*100,]))
    Result.append(Area_sum == np.max(Area_sum))
    
# ERRORをcsvに加えられるようにする
# DateとIDそれぞれで
# Area_sumが閾値以下しかない->unmarked
# Area_sumが大きいものが2つ->max*0.9->duplication?

# Data
for x in range(len(Result)):
    res = np.where(Result[x]==True)[0]
    Value.append(int(res))

ID = Value[7]*10**9+Value[8]*10**8+Value[9]*10**7+Value[10]*10**6+Value[11]*10**5+Value[12]*10**4+Value[13]*10**3+Value[14]*10**2+Value[15]*10**1+Value[16]*10**0
Date = str(Value[0])+str(Value[1])+'/'+str(Value[2])+str(Value[3])+'/'+str(Value[4])+str(Value[5])

# Answer
# Markerに囲まれた範囲を設定する
Marker_Match = cv2.matchTemplate(Marksheet, Marker_ANS, cv2.TM_CCOEFF_NORMED)
Marker_Location = np.where( Marker_Match >= 0.7 ) # 閾値を設定

# 切り出し範囲を設定
Markarea = {}
Markarea['top_x'] = min(Marker_Location[1]) # loc[1]がx軸を表す
Markarea['top_y'] = min(Marker_Location[0]) # loc[0]がx軸を表す
Markarea['bottom_x'] = max(Marker_Location[1])
Markarea['bottom_y'] = max(Marker_Location[0])

# Y軸方向のマーカーのサイズを取り出す
Marker_Answer_Y = Marker_ANS.shape[1]
Marker_Answer_X = Marker_ANS.shape[0]

# 切り出し
# こうすると余白がなくなる
Answer = Marksheet[(Markarea['top_y']+Marker_Answer_Y):Markarea['bottom_y'],Markarea['top_x']:Markarea['bottom_x']+Marker_Answer_X]
cv2.imwrite('Image/Answer.png',Answer)

# Resize
n_col = 5
n_row = 8
Answer_Resize = cv2.resize(Answer, (n_col*100, (n_row+margin_top)*100))
cv2.imwrite('Image/Answer_Resize.png', Answer_Resize)

# Blur
Answer_Blur = cv2.GaussianBlur(Answer_Resize, (5,5), 0)
cv2.imwrite('Image/Answer_Blur.png',Answer_Blur)

# 2値化
RetVal, Answer_Binarization = cv2.threshold(Answer_Blur, 50, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite('Image/Answer_Binarization.png',Answer_Binarization)

# 反転
Answer_Reverse = 255 - Answer_Binarization
cv2.imwrite('Image/Answer_Reverse.png',Answer_Reverse)

# 分割
# for row in range(margin_top, n_row - margin_bottom):
# 結果を入れる配列を用意
Result = []
for row in range(n_row):
    tmp_Answer = Answer_Reverse[row*100:(row+1)*100,]
    cv2.imwrite("PNG/Answer_Tmp%d.png" % row, tmp_Answer)
    Area_sum = []  
    for col in range(n_col):
        Area_sum.append(np.sum(tmp_Answer[:,col*100:(col+1)*100]))
    Result.append(Area_sum == np.max(Area_sum))
    
# ERRORをcsvに加えられるようにする
# DateとAnswerそれぞれで
# Area_sumが閾値以下しかない->unmarked
# Area_sumが大きいものが2つ->max*0.9->duplication?

# Data
Value_ANS = []
nrow_ANS = 2,4,6,8

for x in nrow_ANS:
    res = np.where(Result[x-1]==True)[0]+1
    Value_ANS.append(int(res))

df = pd.DataFrame({'Value': Value_ANS,
                  'Variable': ['Desire', 'Constipation', 'Incontinence', 'Soiling'],
                  'Date': Date,
                  'ChartID': ID})
