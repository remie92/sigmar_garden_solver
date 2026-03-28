from marble_types import marble_types
from PIL import Image
from os import path
class MarbleDetector:
    def __init__(self):
        self.marble_images=[]
        for type in marble_types:
            self.marble_images.append((type,Image.open(path.abspath(f"marble_images/{type}_on.png")).convert("RGB")))
            self.marble_images.append((type,Image.open(path.abspath(f"marble_images/{type}_off.png")).convert("RGB")))
        self.marble_images.append(("empty",Image.open(path.abspath("marble_images/empty.png")).convert("RGB")))
        self.counter=0

    def get_type_from_image(self, image):
    
        best_score = float("inf")
        best_type = None

        img_pixels = image.load()

        # Precompute image color ONCE (important for speed)
        img_color = self.normalize_color(self.avg_color(image))

        for marble_type, ref_img in self.marble_images:
            ref_pixels = ref_img.load()

            # Precompute ref color ONCE
            ref_color = self.normalize_color(self.avg_color(ref_img))
            color_score = self.color_distance(img_color, ref_color)

            # Try small shifts
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    self.counter += 1

                    img_vals = []
                    ref_vals = []

                    for x in range(30):
                        for y in range(30):
                            rx = x + dx
                            ry = y + dy

                            if 0 <= rx < 30 and 0 <= ry < 30:
                                img_vals.append(self.brightness(img_pixels[x, y]))
                                ref_vals.append(self.brightness(ref_pixels[rx, ry]))

                    if not img_vals:
                        continue

                    # Normalize brightness (remove gradient)
                    img_avg = sum(img_vals) / len(img_vals)
                    ref_avg = sum(ref_vals) / len(ref_vals)

                    shape_score = 0
                    for a, b in zip(img_vals, ref_vals):
                        shape_score += abs((a - img_avg) - (b - ref_avg))

                    shape_score /= len(img_vals)

                    # 🔥 COMBINE BOTH SCORES HERE
                    final_score = shape_score * 0.7 + color_score * 0.3

                    if final_score < best_score:
                        best_score = final_score
                        best_type = marble_type

        return best_type
    

    def brightness(self,p):
        return (p[0] + p[1] + p[2]) / 3
    
    def avg_color(self,img):
        pixels = img.load()
        r = g = b = count = 0

        for x in range(img.width):
            for y in range(img.height):
                pr, pg, pb = pixels[x, y]
                r += pr
                g += pg
                b += pb
                count += 1

        return (r / count, g / count, b / count)
    
    def normalize_color(self,c):
        total = c[0] + c[1] + c[2] + 1e-6
        return (c[0]/total, c[1]/total, c[2]/total)
    
    def color_distance(self,c1, c2):
        return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])
            

