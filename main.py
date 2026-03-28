from pynput import mouse
import pyautogui
from PIL import Image
from time import sleep


from board import Board
start_board=Board()





clicks = []
TARGET_WIDTH = 833
TARGET_HEIGHT = 688
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT

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

left = min(screen_x1, screen_x2)
right = max(screen_x1, screen_x2)
top = min(screen_y1, screen_y2)
bottom = max(screen_y1, screen_y2)

width = right - left
height = bottom - top

print(f"Board is {width} pixels wide, and {height} pixels high!")

half_w = min(screen_middle_x - left, right - screen_middle_x)
half_h = min(screen_middle_y - top, bottom - screen_middle_y)

if half_w / half_h > TARGET_RATIO:
    half_w = int(half_h * TARGET_RATIO)
else:
    half_h = int(half_w / TARGET_RATIO)

crop_left = int(screen_middle_x - half_w)
crop_right = int(screen_middle_x + half_w)
crop_top = int(screen_middle_y - half_h)
crop_bottom = int(screen_middle_y + half_h)

print(f"Final crop: {(crop_left, crop_top, crop_right, crop_bottom)}")

full_img = pyautogui.screenshot()

img = full_img.crop((crop_left, crop_top, crop_right, crop_bottom))
img = img.resize((TARGET_WIDTH, TARGET_HEIGHT))

img.show()