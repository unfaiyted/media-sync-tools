from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_gradient(width, height, start, end, angle):
    # Calculate the diagonal length of the image using the Pythagorean theorem
    diagonal = int((width**2 + height**2)**0.5)

    # Create a straight gradient from start to end in a square image
    data = np.zeros((diagonal, diagonal, 3), dtype=np.uint8)
    r, g, b = start
    delta_r, delta_g, delta_b = np.array(end) - np.array(start)
    for x in range(diagonal):
        weight = x / (diagonal - 1)
        data[:, x] = r + weight * delta_r, g + weight * delta_g, b + weight * delta_b

    img = Image.fromarray(data)

    # Rotate by the specified angle
    img = img.rotate(angle)

    # Crop to the original size, centered
    start_x = (diagonal - width) // 2
    start_y = (diagonal - height) // 2
    img = img.crop((start_x, start_y, start_x + width, start_y + height))
    return img



def draw_text(img, text, font_path, color=(255, 255, 255)):
    # Draw text in the center of the image
    draw = ImageDraw.Draw(img)
    width, height = img.size
    font_size = int(width / len(text)) + 8  # adjust this formula as needed
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font)
    position = ((width - text_width) / 2, (height - text_height) / 2)
    draw.text(position, text, font=font, fill=color)
    return img

# Parameters
text = 'Sleeping Shows'
width, height = 400, 600  # size of the image


# #ffffff#ffffff#ffffff
start, end = (233, 0, 4), (88, 76, 76)  # colors for the gradient
font_path = './OpenSans-SemiBold.ttf'  # path to your .ttf font file

# Create image
img = create_gradient(width, height, start, end, -160)
img = draw_text(img, text, font_path)
img.save('output.png', quality=95)
