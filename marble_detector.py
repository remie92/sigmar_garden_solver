import numpy as np
from marble_types import marble_types
from PIL import Image
from os import path


class MarbleDetector:
    def __init__(self):
        self.marble_images = []

        names = [(marble_type, suffix)
                 for marble_type in marble_types
                 for suffix in ("on", "off")]
        names.append(("empty", None))

        for entry in names:
            marble_type, suffix = entry
            filename = (f"{marble_type}_{suffix}.png" if suffix
                        else "empty.png")
            img = Image.open(
                path.abspath(f"marble_images/{filename}")
            ).convert("RGB")

            arr = np.array(img, dtype=np.float32) / 255.0  # shape (H, W, 3), range 0-1
            norm_color = self._normalize_color(arr.mean(axis=(0, 1)))

            self.marble_images.append((marble_type, arr, norm_color))

        self.counter = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_type_from_image(self, image: Image.Image) -> str:
        arr = np.array(image.convert("RGB"), dtype=np.float32) / 255.0
        img_color = self._normalize_color(arr.mean(axis=(0, 1)))

        h, w = arr.shape[:2]
        # Brightness: mean across channels, shape (H, W)
        img_brightness = arr.mean(axis=2)

        best_score = float("inf")
        best_type = None

        for marble_type, ref_arr, ref_color in self.marble_images:
            color_score = self._color_distance(img_color, ref_color)

            ref_brightness = ref_arr.mean(axis=2)

            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    self.counter += 1
                    shape_score = self._shifted_shape_score(
                        img_brightness, ref_brightness, dx, dy, h, w
                    )
                    if shape_score is None:
                        continue

                    # Both scores are now in the same ~0-1 range
                    final_score = shape_score * 0.7 + color_score * 0.3

                    if final_score < best_score:
                        best_score = final_score
                        best_type = marble_type

        if best_type=="earth":
            for marble_type, ref_arr, ref_color in self.marble_images:
                color_score = self._color_distance(img_color, ref_color)

                ref_brightness = ref_arr.mean(axis=2)

                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        self.counter += 1
                        shape_score = self._shifted_shape_score(
                            img_brightness, ref_brightness, dx, dy, h, w
                        )
                        if shape_score is None:
                            continue

                        # Both scores are now in the same ~0-1 range
                        final_score = shape_score * 0.9 + color_score * 0.1
                        if(marble_type=="water"):
                            final_score/=1.4


                        if final_score < best_score:
                            best_score = final_score
                            best_type = marble_type


        return best_type

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _shifted_shape_score(
        img_b: np.ndarray,
        ref_b: np.ndarray,
        dx: int, dy: int,
        h: int, w: int,
    ):
        """Compare brightness patterns with a pixel shift applied to ref."""
        # Compute the overlapping slice for img and shifted ref
        x0_img = max(0, -dx);  x1_img = min(w, w - dx)
        y0_img = max(0, -dy);  y1_img = min(h, h - dy)
        x0_ref = max(0,  dx);  x1_ref = min(w, w + dx)
        y0_ref = max(0,  dy);  y1_ref = min(h, h + dy)

        img_patch = img_b[y0_img:y1_img, x0_img:x1_img]
        ref_patch = ref_b[y0_ref:y1_ref, x0_ref:x1_ref]

        if img_patch.size == 0:
            return None

        # Remove DC offset so we compare shape, not absolute brightness
        img_norm = img_patch - img_patch.mean()
        ref_norm = ref_patch - ref_patch.mean()

        # MAE of normalised brightness — stays in 0-1 range because
        # brightness was already normalised to 0-1
        return float(np.abs(img_norm - ref_norm).mean())

    @staticmethod
    def _normalize_color(c: np.ndarray) -> np.ndarray:
        total = c.sum() + 1e-6
        return c / total

    @staticmethod
    def _color_distance(c1: np.ndarray, c2: np.ndarray) -> float:
        return float(np.abs(c1 - c2).sum())