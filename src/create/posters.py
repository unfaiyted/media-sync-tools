import io
import os
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter


class PosterImageCreator:
    gradient_colors = {
        'red-darkred': ((255, 0, 0), (128, 0, 0)),
        'green-darkgreen': ((0, 255, 0), (0, 128, 0)),
        'blue-darkblue': ((0, 0, 255), (0, 0, 128)),
        'yellow-olive': ((255, 255, 0), (128, 128, 0)),
        'cyan-teal': ((0, 255, 255), (0, 128, 128)),
        'magenta-purple': ((255, 0, 255), (128, 0, 128)),
        'orange-darkorange': ((255, 165, 0), (128, 83, 0)),
        'maroon-darkmaroon': ((128, 0, 0), (64, 0, 0)),
        'olive-darkolive': ((128, 128, 0), (64, 64, 0)),
        'darkgreen-verydarkgreen': ((0, 128, 0), (0, 64, 0)),
        'grey-darkgrey': ((128, 128, 128), (64, 64, 64)),
        'white-grey': ((255, 255, 255), (128, 128, 128)),
    }

    def __init__(self, width: int = 400, height: int = 600 , color: str or tuple = 'random', angle: int = 0,
                 poster=None, # instance of Image
                 font_path: str = './src/resources/fonts/DroneRangerPro-ExtendedBold.ttf'):
        self.width = width
        self.height = height
        if isinstance(color, tuple):
            self.start, self.end = color
        elif isinstance(color, str):
            if (color == 'random'):
                self.start, self.end = self.gradient_colors[
                    list(self.gradient_colors.keys())[np.random.randint(0, len(self.gradient_colors.keys()))]]
            else:
                self.start, self.end = self.gradient_colors[color]
        else:
            raise ValueError("Invalid color type. Must be a named color or a tuple.")
        self.angle = angle
        self.font_path = font_path
        self.unsplash_api_key = 'jKJxjPf88Ui_eiYyMjXxsZMy5H3hL-cQgystWGEcxa8'
        if poster:
            self.image = poster
        else:
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

    def draw_text(self, text, color=(255, 255, 255), offset=(0, 0), border=None, shadow=None):
        draw = ImageDraw.Draw(self.image)
        width, height = self.image.size
        font_size = int(width / len(text)) + 22 if len(text) > 8 else 60
        # print(f'fontsize {font_size} {len(text)}')
        font = ImageFont.truetype(self.font_path, font_size)

        text_size = font.font.getsize(text)
        # print(text_size)
        text_width, text_height = text_size[0][0], text_size[0][1]

        line_spacing = text_height * 1.2

        # print(text_width, text_height)
        # print(width, height,'img width height')

        def draw_with_effects(x, y, line_text):
            # Prepare an empty image with the same size as the original
            shadow_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_layer)

            if shadow:
                shadow_offset, shadow_color, shadow_blur_radius, shadow_opacity = shadow
                r, g, b = shadow_color
                # Draw the shadow text
                shadow_draw.text((x + shadow_offset, y + shadow_offset), line_text, font=font,
                                 fill=(r, g, b, shadow_opacity))

                # Apply Gaussian blur
                shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur_radius))

                # Merge the shadow layer onto the main image
                self.image.paste(shadow_layer, (0, 0), shadow_layer)

            if border:
                border_size, border_color = border
                # Draw text for each side of the border
                for dx in [-border_size, border_size, 0]:
                    for dy in [-border_size, border_size, 0]:
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), line_text, font=font, fill=border_color)

            draw.text((x, y), line_text, font=font, fill=color)

        if text_width > width:
            # Estimate approximately how many characters would fit in the width.
            # Subtract a bit to be safe.
            n_chars = len(text) * width // text_width
            # Split the text by words and assemble lines not exceeding n_chars
            words = text.split()
            lines = ['']
            for word in words:
                if len(lines[-1] + ' ' + word) <= n_chars - 2:
                    lines[-1] += ' ' + word
                else:
                    lines.append(word)

            bad_line = 0
            for i, line in enumerate(lines):
                if line == "":
                    bad_line = bad_line + 1
                    continue
                # Determine the width and height of this line
                # print('text:', line)
                line_width, line_height = font.font.getsize(line)[0]

                # print(f"Line {i+1} - Width: {line_width}, Height: {line_height}")

                # Calculate position for this line
                x = (width - line_width) / 2 + offset[0]
                y = (((height - text_height) / 2) + offset[1])
                y = y + ((i - bad_line) * line_spacing)
                # print(f"Line {i+1} - X: {x}, Y: {y}")
                draw_with_effects(x, y, line)
        else:
            # If the text fits on one line, follow the original logic
            position = [((width - text_width) / 2) + offset[0], ((height - text_height) / 2) + offset[1]]
            # print(f"One-line Text - X: {position[0]}, Y: {position[1]}")
            draw_with_effects(position[0], position[1], text)

    def add_icon(self, icon_path, icon_size=None):
        img = self.create_gradient()
        icon_img = Image.open(icon_path).convert("RGBA")
        icon_img = ImageOps.invert(icon_img)
        if icon_size:
            icon_img = icon_img.resize(icon_size, Image.LANCZOS)

        img_width, img_height = img.size
        icon_width, icon_height = icon_img.size
        icon_x = (img_width - icon_width) // 2
        icon_y = (img_height - icon_height) // 2

        img.paste(icon_img, (icon_x, icon_y), mask=icon_img)
        self.image = img
        return self

    def add_icon_with_text(self, icon_path, text, icon_size=None, text_color=(255, 255, 255), border=None, shadow=None):
        img = self.image
        icon_img = Image.open(icon_path).convert("RGBA")
        if icon_size:
            icon_img = icon_img.resize(icon_size, Image.LANCZOS)
        else:
            icon_img = icon_img.resize((250, 200), Image.LANCZOS)

        img_width, img_height = img.size
        icon_width, icon_height = icon_img.size
        icon_x = (img_width - icon_width) // 2
        icon_y = (img_height - icon_height - 90) // 2
        text_x = (img_width - icon_width) // 2
        text_y_offset = (icon_height / 2) + 5

        img.paste(icon_img, (icon_x, icon_y), mask=icon_img)
        self.draw_text(text, color=text_color, offset=(0, text_y_offset), border=border, shadow=shadow)

        return self

    def add_border(self, border_width=4, border_height=4, border_color=(255, 255, 255)):
        width, height = self.image.size
        crop_width = width - (border_width * 2)
        crop_height = height - (border_height * 2)

        new_img = Image.new('RGB', (width, height), border_color)

        #   4-tuple defining the left, upper, right, and lower pixel
        # Calculate the coordinates of the cropping box

        # Resize the image to the new dimensions
        orig = self.image.resize((crop_width, crop_height))

        # Crop the image using the calculated box

        # Calculate center position
        paste_x = (width - crop_width) // 2
        paste_y = (height - crop_height) // 2
        new_img.paste(orig, (paste_x, paste_y))

        self.image = new_img
        return self

    def fetch_image_from_unsplash(self, search_query):
        headers = {
            "Authorization": f"Client-ID {self.unsplash_api_key}",
        }
        params = {
            "query": search_query,
            "per_page": 1,
        }
        response = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
        if response.status_code != 200:
            print("Failed to fetch images from the Unsplash API.")
            return None

        image_url = response.json()["results"][0]["urls"]["regular"]
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            print("Failed to download the background image.")
            return None

        return Image.open(io.BytesIO(image_response.content))

    def fetch_image_from_path(self, path):
        return Image.open(path)

    def _process_fetched_image(self, background_image):
        # Calculate aspect ratios
        base_aspect_ratio = self.image.width / self.image.height
        background_aspect_ratio = background_image.width / background_image.height

        # Calculate the allowed aspect ratio difference threshold (e.g., 0.1 means 10% difference is allowed)
        aspect_ratio_threshold = 0.1

        # If the aspect ratio difference is within the threshold, just resize without cropping
        if abs(base_aspect_ratio - background_aspect_ratio) < aspect_ratio_threshold:
            background_image = background_image.resize(self.image.size, Image.LANCZOS)

        # If the fetched image is much wider
        elif background_image.width > self.image.width:
            left = (background_image.width - self.image.width) / 2
            right = left + self.image.width
            background_image = background_image.crop((int(left), 0, int(right), background_image.height))
            background_image = background_image.resize(self.image.size, Image.LANCZOS)

        # If the fetched image is much taller
        elif background_image.height > self.image.height:
            top = (background_image.height - self.image.height) / 2
            bottom = top + self.image.height
            background_image = background_image.crop((0, int(top), background_image.width, int(bottom)))
            background_image = background_image.resize(self.image.size, Image.LANCZOS)

        else:
            # For any other cases, just resize to fit the base image
            background_image = background_image.resize(self.image.size, Image.LANCZOS)

        return background_image


    def blend_with_background(self, background_image, blend_alpha=0.5):
        if background_image.size != self.image.size:
            background_image = background_image.resize(self.image.size, Image.LANCZOS)
        blended_image = Image.blend(self.image, background_image, alpha=blend_alpha)
        self.image = blended_image
        # print("Background image added to the poster successfully.")

    def add_background_image_from_query(self, search_query):
        if not search_query:
            print('No search query provided. Skipping background image.')
            return self

        background_image = self.fetch_image_from_unsplash(search_query)
        if background_image:
            processed_bg_image = self._process_fetched_image(background_image)
            self.blend_with_background(processed_bg_image)
        return self

    def add_background_image_from_path(self, path):
        background_image = self.fetch_image_from_path(path)
        # print('Background imag fetche successfully.')
        processed_bg_image = self._process_fetched_image(background_image)
        # print('Background image processed successfully.')
        self.blend_with_background(processed_bg_image)
        # print('Background image added to the poster successfully.')
        return self

    def add_overlay_with_text(self, overlay_text, position='bottom-left', background_color=(255, 255, 0),
                              text_color=(0, 0, 0), transparency=128, corner_radius=10):
        # Use a truetype font
        font = ImageFont.truetype(self.font_path, 18)  # 30 is the font size

        text_width, text_height = font.font.getsize(overlay_text)[0]

        # Adding some padding around the text
        padding = 10
        overlay_width = text_width + 2 * padding
        overlay_height = text_height + 2 * padding

        overlay_color = (background_color[0], background_color[1], background_color[2], transparency)

        # Create the overlay
        overlay = Image.new("RGBA", (overlay_width, overlay_height), overlay_color)

        # Drawing rounded rectangle
        round_rectangle = Image.new("RGBA", (overlay_width, overlay_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(round_rectangle)
        draw.rounded_rectangle((0, 0, overlay_width, overlay_height), radius=corner_radius, fill=background_color)

        # Drawing the text on the overlay
        text_position = (padding, padding)
        draw.text(text_position, overlay_text, font=font, fill=text_color)

        # Applying the rounded rectangle on overlay
        overlay.paste(round_rectangle, (0, 0), round_rectangle)
        # Calculate the position of the overlay
        width, height = self.image.size
        if position == 'bottom-left':
            position = (10, height - 10 - overlay_height)  # 10 is for some padding from the edge
        elif position == 'bottom-right':
            position = (width - overlay_width - 10, height - 10 - overlay_height)
        # You can add more positions as needed

        # Composite the overlay on the image
        self.image.paste(overlay, position, overlay)

        return self

    def resize(self, width, height):
        """
        Resize the image to the specified width and height.

        :param width: New width for the image.
        :param height: New height for the image.
        :return: self
        """
        self.image = self.image.resize((width, height), Image.LANCZOS)
        return self

    def save(self, path, quality=99):
        self.image.convert("RGBA").save(path, quality=quality)
        return self

    def save_original(self, path, quality=99, use_original=False):
        # check if file exists
        if os.path.isfile(path):
            print(f'File {path} already exists. ')
            if use_original:
                print('Using the original file.')
                self.image = Image.open(path).convert("RGBA")
            return self

        self.image.convert("RGBA").save(path, quality=quality)
        return self

    @staticmethod
    def create_emby_poster(path, text, root_path, icon_path=f'resources/tv.png'):
        icon_path = f'{root_path}/{icon_path}'

        width, height = 400, 600
        start, end = (233, 0, 4), (88, 76, 76)
        angle = -160
        font_path = f'{root_path}/resources/OpenSans-SemiBold.ttf'  # path to your .ttf font file

        gradient_creator = PosterImageCreator(width, height, start, end, angle, font_path)
        img = gradient_creator.create_gradient().add_icon_with_text(icon_path, text)

        img.save(path, quality=95)
        return img

# Example usage
# width, height = 400, 600
# start, end = (233, 0, 4), (88, 76, 76)
# angle = -160
#
# font_path = f'./src/resources/fonts/DroneRangerPro-ExtendedBold.ttf'  # path to your .ttf font file
# # poster = PosterImageCreator(width, height, start, end, angle, font_path)
# #img = poster.create_gradient().draw_text('Sleeping Shows');
#
# # img.save('./output.png')
#
#
#
# # poster = PosterImageCreator(width, height, start, end, angle, font_path)
#
# # img = poster.create_gradient()\
# #     .add_background_image(search_query="bedtime")\
# #     .add_icon_with_text('./src/resources/icons/sleep.png', 'Sleeping Shows')\
# #     .add_border()
# #
# # img.save('./output2.png')
#
#
# # poster = PosterImageCreator(400, 600, ((233, 0, 4), (88, 76, 76)), -160, './src/resources/fonts/DroneRangerPro-ExtendedBold.ttf')
#
# search_queries = ["beach", "mountains", "city", "desert", "forest", "river", "ocean", "sunrise", "sunset", "night sky"]
# texts = ["Beach Life", "Mountain High", "City Vibes", "Desert Storm", "Forest Peace", "River Flow", "Ocean Wave", "Sunrise Hope", "Sunset Calm", "Night Mystery"]
# icons = [f"./src/resources/icons/tv.png" for i in range(1, 11)]
#
# for i, color_name in enumerate(PosterImageCreator.gradient_colors):
#     # Create a PosterImageCreator instance with the current color gradient
#     poster = PosterImageCreator(400, 600, color_name, 45)
#
#     # Generate a random poster
#     img = poster.create_gradient() \
#             .add_icon_with_text(icons[i], texts[i]) \
#             .add_border()
#           #  .add_background_image(search_query=search_queries[i]) \
#
#     if not os.path.exists('./examples'):
#             os.makedirs('./examples')
#     img.save(f'./examples/output{i+1}.png')
#
