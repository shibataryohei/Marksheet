PNG_File = PNG_Files[0]
Marksheet = cv2.imread('PNG_Input/'+PNG_File, 0)
Marker_Match = cv2.matchTemplate(Marksheet, Marker_ID, cv2.TM_CCOEFF_NORMED)
Marker_Location = np.where( Marker_Match >= 0.7 ) 
    
Markarea = {}
Markarea['top_x'] = min(Marker_Location[1]) 
Markarea['top_y'] = min(Marker_Location[0]) 
Markarea['bottom_x'] = max(Marker_Location[1])
Markarea['bottom_y'] = max(Marker_Location[0])
    
Marker_ID_Y = Marker_ID.shape[1]
Marker_ID_X = Marker_ID.shape[0]
    
ID = Marksheet[(Markarea['top_y']+Marker_ID_Y):Markarea['bottom_y'],Markarea['top_x']:Markarea['bottom_x']+Marker_ID_X]
cv2.imwrite('Temp/ID.png',ID_Reverse)

n_col = 17
n_row = 10
margin_top = 4
ID_Resize = cv2.resize(ID, (n_col*100, (n_row+margin_top)*100))
    
ID_Blur = cv2.GaussianBlur(ID_Resize, (25,25), 0)
RetVal, ID_Binarization = cv2.threshold(ID_Blur, 50, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ID_Reverse = 255 - ID_Binarization
    
Result = []
for col in range(n_col):
    tmp_ID = ID_Reverse[:,col*100:(col+1)*100]
    Area_sum = []  
    for row in range(margin_top, margin_top+n_row):
        Area_sum.append(np.sum(tmp_ID[row*100:(row+1)*100,]))
    Result.append(Area_sum == np.max(Area_sum))
    
Value = []
for x in [0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16]:
    res = np.where(Result[x]==True)[0]
    Value.append(int(res))
    
ChartID = Value[6]*10**9+Value[7]*10**8+Value[8]*10**7+Value[9]*10**6+Value[10]*10**5+Value[11]*10**4+Value[12]*10**3+Value[13]*10**2+Value[14]*10**1+Value[15]*10**0
Date = str(Value[0])+str(Value[1])+'/'+str(Value[2])+str(Value[3])+'/'+str(Value[4])+str(Value[5])
    
Marker_Match = cv2.matchTemplate(Marksheet, Marker_ANS, cv2.TM_CCOEFF_NORMED)
Marker_Location = np.where( Marker_Match >= 0.7 ) 
    
Markarea = {}
Markarea['top_x'] = min(Marker_Location[1]) 
Markarea['top_y'] = min(Marker_Location[0]) 
Markarea['bottom_x'] = max(Marker_Location[1])
Markarea['bottom_y'] = max(Marker_Location[0])
    
Marker_Answer_Y = Marker_ANS.shape[1]
Marker_Answer_X = Marker_ANS.shape[0]
    
Answer = Marksheet[(Markarea['top_y']+Marker_Answer_Y):Markarea['bottom_y'],Markarea['top_x']:Markarea['bottom_x']+Marker_Answer_X]
cv2.imwrite('Temp/Answer.png',Answer_Resize)
    
n_col = 5
n_row = 8
Answer_Resize = cv2.resize(Answer, (n_col*100, (n_row)*100))
Answer_Blur = cv2.GaussianBlur(Answer_Resize, (5,5), 0)
RetVal, Answer_Binarization = cv2.threshold(Answer_Blur, 50, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
Answer_Reverse = 255 - Answer_Binarization
Result = []
for row in range(n_row):
    tmp_Answer = Answer_Reverse[row*100:(row+1)*100,]
    cv2.imwrite("Temp/Answer_Tmp%d.png" % row, tmp_Answer)
    Area_sum = []  
    for col in range(n_col):
        Area_sum.append(np.sum(tmp_Answer[:,col*100:(col+1)*100]))
    Result.append(Area_sum == np.max(Area_sum))
    
Value_ANS = []
nrow_ANS = 2,4,6,8
    
for x in nrow_ANS:
    res = np.where(Result[x-1]==True)[0]+1
    Value_ANS.append(int(res))
    
Data = pd.DataFrame({'Value': Value_ANS,'Variable': ['Desire', 'Constipation', 'Incontinence', 'Soiling'],'Date': Date,'ChartID': ID,'PATH': PNG_File})
DataFrame = DataFrame.append(Data)
Log = open('Log.text', 'w') 
Log.write(PNG_File) 
Log.close
