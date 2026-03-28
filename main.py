STATIC_SCREEN_POSITIONS=True


from pynput import mouse
import pyautogui
from PIL import Image,ImageDraw, ImageFont
from time import sleep


from board import Board
start_board=Board()






clicks = []
TARGET_WIDTH = 833
TARGET_HEIGHT = 688
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT

screen_start_height=59
screen_middle_width=TARGET_WIDTH/2
screen_vertical_spacing=(630-59)/10
screen_horizontal_spacing=(747-84)/10

if STATIC_SCREEN_POSITIONS==False:
    def on_click(x, y, button, pressed):
        if pressed:
            print(f"Clicked at: ({x}, {y})")
            clicks.append((x, y))
            if len(clicks) == 3:
                return False  

    with mouse.Listener(on_click=on_click) as listener:
        print("Click the top left of the dark background, and then the center dot of the golden marble. Lastly, the bottom right. The border of the dark triangles count as the background")
        listener.join()
else:
    clicks.append((2722, 162))
    clicks.append((3138, 505))
    clicks.append((3556, 850))


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

numbered_img=img.copy()

draw = ImageDraw.Draw(numbered_img)

try:
    font = ImageFont.truetype("arial.ttf", 20)
except:
    font = ImageFont.load_default()

counter = 0

for i in range(0, 11):
    i_center_dist = abs(5 - i)
    row_size = 11 - i_center_dist

    for j in range(0, row_size):
        middle_j = row_size / 2 - 0.5

        pixel_x = int(screen_middle_width + (j - middle_j) * screen_horizontal_spacing)
        pixel_y = int(i * screen_vertical_spacing + screen_start_height)

        text = str(counter)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(
            (pixel_x - text_w // 2, pixel_y - text_h // 2),
            text,
            fill=(255, 0, 0),
            font=font
        )

        counter += 1

numbered_img.show()
img.show()
