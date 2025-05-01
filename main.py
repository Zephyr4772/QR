import qrcode
import numpy as np
import cv2
import random
from datetime import datetime
from PIL import Image

COLOR_SCHEMES = [
    ((255, 0, 0), (255, 255, 0)),  # Red to Yellow
    ((0, 0, 255), (75, 0, 130)),  # Blue to Indigo
    ((0, 255, 0), (0, 128, 128)),  # Green to Teal
    ((255, 20, 147), (75, 0, 130)),  # Deep Pink to Indigo
    ((255, 165, 0), (255, 69, 0)),  # Orange to Red
    ((128, 0, 128), (0, 255, 255)),  # Purple to Cyan
    ((255, 192, 203), (0, 0, 128)),  # Pink to Navy
    ((0, 0, 0), (128, 128, 128)),  # Black to Gray
    ((255, 223, 0), (255, 105, 180)),  # Gold to Hot Pink
    ((0, 191, 255), (138, 43, 226)),  # Deep Sky Blue to Blue Violet
    ((173, 255, 47), (255, 69, 0)),  # Green Yellow to Red Orange
    ((70, 130, 180), (238, 130, 238)),  # Steel Blue to Violet
    ((186, 85, 211), (255, 140, 0)),  # Medium Orchid to Dark Orange
    ((60, 179, 113), (255, 105, 180)),  # Medium Sea Green to Hot Pink
    ((0, 250, 154), (148, 0, 211)),  # Medium Spring Green to Dark Violet
    ((240, 128, 128), (0, 206, 209)),  # Light Coral to Dark Turquoise
    ((255, 99, 71), (106, 90, 205)),  # Tomato to Slate Blue
    ((72, 209, 204), (255, 20, 147)),  # Medium Turquoise to Deep Pink
    ((139, 0, 139), (0, 255, 127)),  # Dark Magenta to Spring Green
    ((47, 79, 79), (173, 216, 230))  # Dark Slate Gray to Light Blue
]

def create_gradient(qr_img, start_rgb, end_rgb):
    qr_array = np.array(qr_img.convert("L"))
    height, width = qr_array.shape
    gradient_layer = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        blend_ratio = y / height
        transition_color = [
            int(start_rgb[i] * (1 - blend_ratio) + end_rgb[i] * blend_ratio) for i in range(3)
        ]
        gradient_layer[y, :, :] = transition_color
    black_mask = qr_array == 0
    qr_final = np.stack([qr_array] * 3, axis=-1)
    qr_final[black_mask] = gradient_layer[black_mask]
    return cv2.cvtColor(qr_final, cv2.COLOR_RGB2BGR)

def generate_qr_code(input_text):
    qr_code = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr_code.add_data(input_text)
    qr_code.make(fit=True)
    qr_base = qr_code.make_image(fill_color="black", back_color="white")
    start_color, end_color = random.choice(COLOR_SCHEMES)
    qr_colored = create_gradient(qr_base, start_color, end_color)
    qr_colored = Image.fromarray(qr_colored)
    file_name = f"qrcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    qr_colored.save(file_name)
    print(f"🎨 QR code successfully saved as {file_name}")

if __name__ == "__main__":
    text_input = input("Enter text or URL for the QR code: ")
    generate_qr_code(text_input)
