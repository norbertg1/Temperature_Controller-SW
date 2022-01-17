import pyautogui

#pyautogui.click(300, 300)
pyautogui.moveTo(300, 300, 3)
#pyautogui.click()
location = pyautogui.locateCenterOnScreen('start.png', grayscale=True, confidence=.7)
if location is None: 
    print ("not found")
print (location)
pyautogui.moveTo(location.x, location.y, 3)
pyautogui.click()
pyautogui.write("valami", interval=0.1)
pyautogui.press('Enter')
pyautogui.hotkey('alt', 'tab')

