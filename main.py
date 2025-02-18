from PIL import Image, ImageDraw, ImageFont
import os
import random

def add_text_watermark(input_image_path, output_image_path, text="Activaarts", font_size=150, opacity=120):
    """Adds a faint, scratched, and slightly rotated text watermark at 1/3 from the bottom and 1/4 from the right side of a painting."""
    image = Image.open(input_image_path).convert("RGBA")
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(watermark_layer)
    try:
        font = ImageFont.truetype("impact.ttf", font_size)  # Using a bold and shouting font
    except IOError:
        font = ImageFont.load_default()
    
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    position = (int(image.width * (3/4)) - text_width // 2, int(image.height * (2/3)) - text_height // 2)
    
    # Rotate the watermark slightly
    temp_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_layer)
    
    # Create a scratched effect by adding random noise around the text
    outline_color = (50, 50, 50, opacity)  # Dark gray outline to make it faint
    offset = 5
    for _ in range(10):  # Adding noise for a scratched effect
        noise_x = random.randint(-10, 10)
        noise_y = random.randint(-10, 10)
        temp_draw.text((position[0] + noise_x, position[1] + noise_y), text, font=font, fill=outline_color)
    
    # Add main text with lower opacity to make it faint
    temp_draw.text(position, text, fill=(200, 200, 200, opacity), font=font)  # Light gray for a subtle effect
    
    # Rotate the watermark layer
    temp_layer = temp_layer.rotate(-15, expand=1)
    
    watermark_layer.paste(temp_layer, (0, 0), temp_layer)
    
    watermarked_image = Image.alpha_composite(image, watermark_layer)
    watermarked_image.convert("RGB").save(output_image_path, "JPEG")
    print(f"Watermark added to {output_image_path}")

def process_folder(input_folder, output_folder, font_size=150, opacity=120):
    """Processes all paintings in a folder and applies a faint, scratched text watermark."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            add_text_watermark(input_path, output_path, font_size=font_size, opacity=opacity)

if __name__ == "__main__":
    input_folder = r"C:\Users\HP\Downloads\bootstrap\bootstrap-ecommerce\activaarts\public\storage\products"  # Change to your folder path
    output_folder = r"C:\Users\HP\Pictures\Add Watermark"
    
    process_folder(input_folder, output_folder, font_size=150, opacity=120)
