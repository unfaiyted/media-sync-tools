import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


class PosterImageCreator:

    def __init__(self, width, height, start, end, angle, font_path):
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.angle = angle
        self.font_path = font_path
        print(self.font_path)
        self.image = Image.new('RGBA', (width, height))


    def create_gradient(self):
        diagonal = int((self.width ** 2 + self.height ** 2) ** 0.5)
        data = np.zeros((diagonal, diagonal, 3), dtype=np.uint8)
        r, g, b = self.start
        delta_r, delta_g, delta_b = np.array(self.end) - np.array(self.start)
        for x in range(diagonal):
            weight = x / (diagonal - 1)
            data[:, x] = r + weight * delta_r, g + weight * delta_g, b + weight * delta_b

        img = Image.fromarray(data)
        img = img.rotate(self.angle)
        start_x = (diagonal - self.width) // 2
        start_y = (diagonal - self.height) // 2
        img = img.crop((start_x, start_y, start_x + self.width, start_y + self.height))
        self.image = img
        return self


    def draw_text(self, text, color=(255, 255, 255), offset=(0, 0)):
        draw = ImageDraw.Draw(self.image)
        width, height = self.image.size
        font_size = int(width / len(text)) + 24
        font = ImageFont.truetype(self.font_path, font_size)
        print(font, font.getlength("hello"), font.font.getsize("hello"))
        print(font.font.getsize(text), text)

        text_size = font.font.getsize(text)

        text_width, text_height = text_size[0], text_size[1]
        print(text_width[0], text_height[1])
        print(width, height,'img width height')
        position = [((width - text_width[0]) / 2) + offset[0], ((height - text_height[1]) / 2) + offset[1]]
        draw.text(position, text, font=font, fill=color)
        return self

    def add_icon(self, icon_path, icon_size=None):
        img = self.create_gradient()
        icon_img = Image.open(icon_path).convert("RGBA")
        icon_img = ImageOps.invert(icon_img)
        if icon_size:
            icon_img = icon_img.resize(icon_size)

        img_width, img_height = img.size
        icon_width, icon_height = icon_img.size
        icon_x = (img_width - icon_width) // 2
        icon_y = (img_height - icon_height) // 2


        img.paste(icon_img, (icon_x, icon_y), mask=icon_img)
        self.image = img
        return self

    def add_icon_with_text(self, icon_path, text, icon_size=None, text_color=(255, 255, 255)):
        img = self.image
        icon_img = Image.open(icon_path).convert("RGBA")
        if icon_size:
            icon_img = icon_img.resize(icon_size)
        else:
            icon_img = icon_img.resize((300, 250))

        img_width, img_height = img.size
        icon_width, icon_height = icon_img.size
        icon_x = (img_width - icon_width) // 2
        icon_y = (img_height - icon_height - 90) // 2
        text_x = (img_width - icon_width) // 2
        text_y_offset = (icon_height / 2) + 20

        img.paste(icon_img, (icon_x, icon_y), mask=icon_img)
        self.draw_text(text, color=text_color, offset=(0, text_y_offset))

        return self

    def add_border(self, border_width=4, border_height=4, border_color=(0, 0, 0)):
        width, height = self.image.size
        crop_width = width - border_width * 2
        crop_height = height - border_height * 2

        new_img = Image.new('RGB', (width, height), border_color)

     #   4-tuple defining the left, upper, right, and lower pixel
        left = border_width
        right = crop_width
        top = border_height
        bottom = crop_height

        orig = self.image.crop((left, top, right, bottom))

        new_img.paste(orig, (border_width, border_width))

        self.image = new_img
        return self

    def save(self, path):
            self.image.save(path)
            return self


# Example usage
# width, height = 400, 600
# start, end = (233, 0, 4), (88, 76, 76)
# angle = -160
# font_path = f'/resources/OpenSans-SemiBold.ttf'  # path to your .ttf font file
#
# gradient_creator = PosterImageCreator(width, height, start, end, angle, font_path)
# img = gradient_creator.create_gradient().draw_text('Sleeping Shows');
#
# img.save('./output.png')
#
#
#
# gradient_creator = PosterImageCreator(width, height, start, end, angle, font_path)
#
# img = gradient_creator.create_gradient().add_icon_with_text('./resources/sleep.png', 'Sleeping Shows').add_border()
#
# img.save('./output2.png')

