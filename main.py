STATIC_SCREEN_POSITIONS=True

from pynput import mouse
import pyautogui
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import time
from marble_detector import MarbleDetector
from marble_types import marble_types
from board import Board
from solver import Solver
from rules import type_to_index

start_board = Board()
marble_detector = MarbleDetector()

clicks = []
TARGET_WIDTH = 833
TARGET_HEIGHT = 688
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT

screen_start_height = 59
screen_middle_width = TARGET_WIDTH / 2
screen_vertical_spacing = (630 - 59) / 10
screen_horizontal_spacing = (747 - 84) / 10

if STATIC_SCREEN_POSITIONS == False:
    def on_click(x, y, button, pressed):
        if pressed:
            clicks.append((x, y))
            if len(clicks) == 3:
                return False

    with mouse.Listener(on_click=on_click) as listener:
        print("Click top-left, center, bottom-right")
        listener.join()
else:
    clicks.append((2722, 162))
    clicks.append((3138, 505))
    clicks.append((3556, 850))

(screen_x1, screen_y1), (screen_middle_x, screen_middle_y), (screen_x2, screen_y2) = clicks

left = min(screen_x1, screen_x2)
right = max(screen_x1, screen_x2)
top = min(screen_y1, screen_y2)
bottom = max(screen_y1, screen_y2)

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

full_img = pyautogui.screenshot()
img = full_img.crop((crop_left, crop_top, crop_right, crop_bottom))
img = img.resize((TARGET_WIDTH, TARGET_HEIGHT))

# detection storage
positions = []
detected_types = []

for i in range(0, 11):
    i_center_dist = abs(5 - i)
    row_size = 11 - i_center_dist

    for j in range(0, row_size):
        middle_j = row_size / 2 - 0.5

        pixel_x = int(screen_middle_width + (j - middle_j) * screen_horizontal_spacing)
        pixel_y = int(i * screen_vertical_spacing + screen_start_height)

        detection_size = 30
        half = detection_size // 2

        cropped = img.crop((pixel_x - half, pixel_y - half, pixel_x + half, pixel_y + half))
        m_type = marble_detector.get_type_from_image(cropped)

        positions.append((pixel_x, pixel_y))
        detected_types.append(m_type)




# ---------------- GUI ----------------
selected_index = None
final_types = None

root = tk.Tk()
root.title("Marble Editor")

canvas = tk.Canvas(root, width=TARGET_WIDTH, height=TARGET_HEIGHT)
canvas.pack()

img_tk = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, anchor="nw", image=img_tk)

highlight = None
text_items = []

# draw all detected types
for i, (x, y) in enumerate(positions):
    txt = canvas.create_text(x, y, text=detected_types[i], fill="red")
    text_items.append(txt)

label_var = tk.StringVar()
label = tk.Label(root, textvariable=label_var)
label.pack()


def draw_highlight(idx):
    global highlight
    if highlight:
        canvas.delete(highlight)

    x, y = positions[idx]
    r = 15
    highlight = canvas.create_oval(x - r, y - r, x + r, y + r, outline="red", width=2)


def update_text(idx):
    canvas.itemconfig(text_items[idx], text=detected_types[idx])


def on_click(event):
    global selected_index
    x, y = event.x, event.y

    for i, (px, py) in enumerate(positions):
        if abs(px - x) < 15 and abs(py - y) < 15:
            selected_index = i
            draw_highlight(i)
            label_var.set(f"Selected {i}: {detected_types[i]}")
            return


def change_type(t):
    if selected_index is None:
        return

    detected_types[selected_index] = t
    update_text(selected_index)
    label_var.set(f"Updated {selected_index} -> {t}")


canvas.bind("<Button-1>", on_click)

frame = tk.Frame(root)
frame.pack()

for t in marble_types:
    btn = tk.Button(frame, text=t, command=lambda t=t: change_type(t))
    btn.pack(side="left")


def finish():
    global final_types
    final_types = detected_types.copy()
    root.destroy()

btn_done = tk.Button(root, text="Done", command=finish)
btn_done.pack()

root.mainloop()




#Finally doing some calculating!
for i in range(len(final_types)):
    start_board.set_type(type_to_index.get(final_types[i]),i)
print (start_board)

solver=Solver()
solver.set_board(start_board)
winning_moves=solver.solve_board()




def index_to_screen_pos(index):
    """Convert a marble board index to an absolute screen coordinate."""
    img_x, img_y = positions[index]

    # Reverse the resize: map image pixels back to crop-space pixels
    crop_w = crop_right - crop_left
    crop_h = crop_bottom - crop_top

    screen_x = crop_left + (img_x / TARGET_WIDTH) * crop_w
    screen_y = crop_top  + (img_y / TARGET_HEIGHT) * crop_h

    return int(screen_x), int(screen_y)


def click_marble(index, delay=0.2):
    """Move to and left-click a marble by its board index."""
    x, y = index_to_screen_pos(index)
    pyautogui.moveTo(x, y, duration=0.15)
    pyautogui.click(x, y)
    pyautogui.sleep(delay)

for i in range(10,0,-1):
    print(f"Starting in {i} seconds!")
    time.sleep(1)

for coord in winning_moves:
    index1,index2=coord
    click_marble(index1)
    click_marble(index2)