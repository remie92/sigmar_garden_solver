from pynput import mouse
import pyautogui
from PIL import Image
from time import sleep


from board import Board
start_board=Board()





clicks = []

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Clicked at: ({x}, {y})")
        clicks.append((x, y))
        if len(clicks) == 3:
            return False  

with mouse.Listener(on_click=on_click) as listener:
    print("Click the top left of the dark background, and then the center dot of the golden marble. Lastly, the bottom right. The border of the dark triangles count as the background")
    listener.join()


(screen_x1,screen_y1),(screen_middle_x,screen_middle_y),(screen_x2,screen_y2)= clicks
print(screen_x1,screen_y1,screen_x2,screen_y2)

left = min(screen_x1,screen_x2)
top = min(screen_y1,screen_y2)
right = max(screen_x1,screen_x2)
bottom = max(screen_y1,screen_y2)

width = right - left
height = bottom - top

print(f"Board is {width} pixels wide, and {height} pixels high!")


screenshot = pyautogui.screenshot(region=(left, top, width, height))


resized = screenshot.resize((833,688))

resized.show()