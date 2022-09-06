import pyautogui
import time 

sw, sh = pyautogui.size()
l = 0 

while True: 
	if l == 1:
		x, y = -1248, -391
		pyautogui.moveTo(x, y)
		pyautogui.doubleClick()
		l = 0
		time.sleep(15)
	elif l == 0:
		x, y = -1200, -400
		pyautogui.moveTo(x, y)
		pyautogui.doubleClick()
		l = 1
		time.sleep(15)
	
