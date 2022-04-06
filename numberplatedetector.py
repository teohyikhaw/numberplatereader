import cv2
import pytesseract

#############################
frameWidth = 640
frameHeight = 480
plateCascade = cv2.CascadeClassifier("resources/haarcascades/haarcascade_russian_plate_number.xml")
minArea = 200
color = (255,0,255)
#############################
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth) #width
cap.set(4,frameHeight) #length
cap.set(10,150) #brightness
count = 0
while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade.detectMultiScale(imgGray,1.1,10)
    for(x,y,w,h) in numberPlates:
        area = w*h
        if area>minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(img,"Number Plate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,color,2)
            imgRoi = img[y:y+h,x:x+w]
            imgProcess = cv2.medianBlur(cv2.threshold(imgGray[y:y+h,x:x+w],0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1],3)
            text = pytesseract.image_to_string(imgProcess)
            print(text)
            cv2.putText(img,text,(x,y+h),cv2.FONT_HERSHEY_COMPLEX,1,color,2)
            cv2.imshow("ROI",imgRoi)

    cv2.imshow("Result",img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("resources/scanned/noplate_"+str(count)+".jpg",imgRoi)
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,"Scan Saved",(150,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(500)
        count+=1