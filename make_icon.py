from PIL import Image, ImageDraw, ImageFont
import os

def make_icon():
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Rounded background
        padding = int(size * 0.04)
        radius = int(size * 0.18)
        draw.rounded_rectangle([padding, padding, size - padding, size - padding],
                                radius=radius, fill=(13, 13, 13, 255))

        # Font size relative to icon size
        font_size = int(size * 0.58)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

        # Draw B in white
        b_x = int(size * 0.07)
        b_y = int(size * 0.08)
        draw.text((b_x, b_y), "B", font=font, fill=(240, 240, 240, 255))

        # Get B width to position H
        b_bbox = draw.textbbox((b_x, b_y), "B", font=font)
        b_width = b_bbox[2] - b_bbox[0]

        # Draw H in green, slightly overlapping B
        h_x = b_x + int(b_width * 0.72)
        draw.text((h_x, b_y), "H", font=font, fill=(0, 230, 118, 255))

        images.append(img)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'buildhaus.ico')
    images[0].save(out, format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
    print(f"Saved: {out}")

make_icon()
