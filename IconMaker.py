from PIL import Image, ImageDraw
from Logger import createLogger
import sys
import os 
import re

ic_launcher_sizes = [
    {"dirName": "mipmap-xxxhdpi", "values": (192, 192)},
    {"dirName": "mipmap-xxhdpi", "values": (144, 144)},
    {"dirName": "mipmap-xhdpi", "values": (96, 96)},
    {"dirName": "mipmap-hdpi", "values": (72, 72)},
    {"dirName": "mipmap-mdpi", "values": (48, 48)}
]

ic_notification_sizes = [
    {"dirName": "mipmap-xxhdpi", "values": (72, 72)},
    {"dirName": "mipmap-xhdpi", "values": (48, 48)},
    {"dirName": "mipmap-hdpi", "values": (36, 36)},
    {"dirName": "mipmap-mdpi", "values": (24, 24)}
]

logger = createLogger("IconMaker")

def makeIcons(image, icon_type=ic_launcher_sizes, add_background=False):
    sizes = ic_launcher_sizes if icon_type == 'launcher' else ic_notification_sizes
    iconName = 'ic_launcher.png' if icon_type == 'launcher' else 'ic_notification.png'
    
    try:
        for size in sizes:
            resized_image = image.copy()
            resized_image.thumbnail(size["values"])

            if add_background:
                background_color = (255, 255, 255)
                if iconName.endswith('round'):
                    background_radius = 10
                    rounded_image = Image.new('RGBA', size["values"], background_color)
                    mask = Image.new('L', size["values"], 0)
                    draw = ImageDraw.Draw(mask)
                    draw.rounded_rectangle((0, 0, size["values"][0], size["values"][1]), background_radius, fill=255)
                    rounded_image.paste(resized_image, mask=mask)
                    resized_image = rounded_image
                else:
                    background_image = Image.new('RGB', size["values"], background_color)
                    background_image.paste(resized_image, ((size["values"][0] - resized_image.width) // 2, (size["values"][1] - resized_image.height) // 2))
                    resized_image = background_image
            
            os.makedirs(size["dirName"], exist_ok=True)
            resized_image.save(os.path.join(size["dirName"], iconName))
            
            if icon_type == 'launcher':
                resized_image.save(os.path.join(size["dirName"], 'ic_launcher_round.png'))

        logger.info("Done making icons.")
    except:
        logger.error("Failed to make icons!")

def main():
    if len(sys.argv) < 3:
        url = input("Please enter the URL of the desired image:\n")
        icon_type = input("Type \"launcher\" or \"notification\" to specify the icon type:\n")
        add_background = input("Add a white square background? (y/n): ")
    else:
        url, icon_type = sys.argv[1:3]
        add_background = sys.argv[3] if len(sys.argv) >= 4 else 'n'
    
    add_background = add_background.lower() == 'y'
    
    if icon_type == 'launcher':
        sizes = ic_launcher_sizes
    else:
        sizes = ic_notification_sizes
    
    try:
        image = Image.open(url)
    except:
        logger.error("Failed to open the specified URL!")
        return
    
    if not re.search("^.*\.png|\.jpg|\.jpeg$", url):
        logger.error("Selected file is not an image!")
    elif (image.size[0] < sizes[0]["values"][0] or image.size[1] < sizes[0]["values"][1]):
        logger.error("Selected image is too small. Please select an image with a width and height of at least " + str(sizes[0]["values"][0]) + " pixels.")
    else:
        if re.search("^.*\.jpg|\.jpeg$", url):
            logger.warning("Selected file format is a non-PNG image. Consider using PNG formatted images for icons as Android documents suggest so.")
        if (image.size[0] != image.size[1]):
            logger.warning("Selected file does not have equal width and height. Consider using a square image to prevent distortion.")
        makeIcons(image, icon_type, add_background)

main()
