
import cv2 as cv2

#helper thing to get coordinates from frames

def click_event(event,x,y,flags,params):

  if event == cv2.EVENT_LBUTTONDOWN:
    
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(img, str(x) + ',' + str(y), (x,y), font, 1, (255,0,0),2)
    cv2.imshow('image', img)

if __name__ == '__main__':

  path = r"C:\Users\henry\Downloads\img2465.png"
  img = cv2.imread(path, 0)
  cv2.imshow('image', img)
  cv2.setMouseCallback('image', click_event)
  cv2.waitKey(0)
  cv2.destroyAllWindows()