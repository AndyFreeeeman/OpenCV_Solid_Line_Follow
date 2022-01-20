import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# 開啟網路攝影機 or 目標影片
cap = cv2.VideoCapture(0)

# 設定影像尺寸
width = 1280
height = 720

# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while(cap.isOpened()):
    # 讀取一幅影格
    ret, original_image = cap.read()
    ret, image = cap.read()

  # 若讀取至影片結尾，則跳出
    if ret == False:
        break

  # 模糊處理
    blur = cv2.blur(image, (4, 4))
    
  # 使用型態轉換函數去除雜訊
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)
    

  # 挑出黑色
    image = cv2.inRange(image, (0,0,0), (50,50,50))
    
    
  # 影像侵蝕 膨脹
    image = cv2.erode(image, kernel, iterations=5)
    image = cv2.dilate(image, kernel, iterations=9)	   
    
    copy = image
    
  # 找輪廓
    contours_blk, hierarchy_blk = cv2.findContours(copy , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours_blk) > 0:
        
        # 生成最小矩形
        blackbox = cv2.minAreaRect(contours_blk[0])
        
        (x_min, y_min), (w_min, h_min), ang = blackbox
        
        #if ang < -45 :
        #    ang = 90 + ang
            
        #if w_min < h_min and ang > 0:
        #    ang = (90-ang)*-1
            
        #if w_min > h_min and ang < 0:
        #    ang = 90 + ang
            
        setpoint = 640
        
        error = int(x_min - setpoint) 
        
        ang = int(ang)
        
        box = cv2.boxPoints(blackbox)
        
        box = np.int0(box)
        
        cv2.drawContours(original_image,[box],0,(0,0,255),3)
        
        cv2.putText(original_image,"Angle:"+str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.putText(original_image,"Offset:"+str(error),(10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        cv2.line(original_image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)
    

  # 顯示偵測結果影像
    cv2.imshow('result', original_image)

    if cv2.waitKey(1) & 0xFF == ord('0'):
        break  

cap.release()
cv2.destroyAllWindows()
