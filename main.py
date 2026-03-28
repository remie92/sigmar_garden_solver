from pynput import mouse
from time import sleep


from board import Board
start_board=Board()





clicks = []

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Clicked at: ({x}, {y})")
        clicks.append((x, y))
        if len(clicks) == 2:
            return False  

with mouse.Listener(on_click=on_click) as listener:
    print("Click the top left of the dark background, and  then the bottom right. The border of the dark triangles count as the background.")
    listener.join()


(screen_x1,screen_y1),(screen_x2,screen_y2)= clicks
print(screen_x1,screen_y1,screen_x2,screen_y2)