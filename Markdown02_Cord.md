import cv2
Answer = cv2.imread('PNG/Answer2.png', 0)

n_col = 7 # マークの列数
n_row = 7 # マークの行数
margin_top = 3 # 上余白行数
margin_bottom = 1 # 下余白行数

n_row_total = n_row + margin_top + margin_bottom # 行数 (マーク行 7行 + 上余白 3行 + 下余白 1行)

Answer_Resize = cv2.resize(Answer, (n_col*100, n_row_total*100))
cv2.imwrite('PNG/Answer_Resize.png', Answer_Resize)

Answer_Blur = cv2.GaussianBlur(Answer_Resize, (5,5), 0)
cv2.imwrite('PNG/Answer_Blur.png',Answer_Blur)

RetVal, Answer_Binarization = cv2.threshold(Answer_Blur, 50, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

Answer_Reverse = 255 - Answer_Binarization

cv2.imwrite('PNG/Answer_Reverse.png',Answer_Reverse)