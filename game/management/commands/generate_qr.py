from game.models import *
from django.core.management.base import BaseCommand
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import shutil


class Command(BaseCommand):

    def generate_qr_with_text(self, url, text, output_file="qrcode.png"):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,  # automatically adjusts size if None
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Font settings (default PIL font if no TTF available)
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../static/game/fonts/font.ttf"))
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 20)
            except Exception as e:
                print(f"Error loading custom font: {e}. Using default font.")
                font = ImageFont.load_default()
        else:
            print(f"Custom font not found at {font_path}, using default font.")
            font = ImageFont.load_default()

        # Measure text size
        draw = ImageDraw.Draw(qr_img)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top

        # Create new image with extra space for text
        new_img = Image.new("RGB", (qr_img.width, qr_img.height + text_height + 20), "white")
        new_img.paste(qr_img, (0, 0))

        # Draw text centered under QR
        draw = ImageDraw.Draw(new_img)
        text_x = (new_img.width - text_width) // 2
        text_y = qr_img.height - 20
        draw.text((text_x, text_y), text, fill="black", font=font)

        # Save result
        new_img.save(output_file)
        print(f"QR code saved as {output_file}")

    
    def handle(self, *args, **options):
        print("Generating QR codes...")

        # clearing_folder
        qr_folder = "qr_codes"
        if os.path.exists(qr_folder):
            shutil.rmtree(qr_folder)
        os.makedirs(qr_folder)


        server_url = "http://164.92.231.44:3000/"
        server_url += "visit/"

        for point in GraphPoint.objects.all():
            url = server_url + point.identifier
            output_file = os.path.join(qr_folder, f"{point.identifier}.png")
            self.generate_qr_with_text(url, point.default_name, output_file)
        print("QR code generation completed.")