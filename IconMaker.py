from PIL import Image
from Logger import createLogger
import sys
import os 
import re

# These are the sizes that an Android project declares for app icons
ic_launcher_sizes = [
    {"dirName": "mipmap-xxxhdpi", "values": (192,192)},
    {"dirName": "mipmap-xxhdpi", "values": (144,144)},
    {"dirName": "mipmap-xhdpi", "values": (96,96)},
    {"dirName": "mipmap-hdpi", "values": (72,72)},
    {"dirName": "mipmap-mdpi", "values": (48,48)}
]

ic_notification_sizes = [
    {"dirName": "mipmap-xxhdpi", "values": (72,72)},
    {"dirName": "mipmap-xhdpi", "values": (48,48)},
    {"dirName": "mipmap-hdpi", "values": (36,36)},
    {"dirName": "mipmap-mdpi", "values": (24,24)}
]

logger = createLogger("IconMaker")

def makeIcons(image, type = ic_launcher_sizes):
    if type == 'launcher':
        sizes = ic_launcher_sizes
        iconName = 'ic_launcher.png'
        roundIconName = 'ic_launcher_round.png'
    else:
        sizes = ic_notification_sizes
        iconName = 'ic_notification.png'

    try:
        for i in range(len(sizes)):
            image.thumbnail(sizes[i]["values"])
            os.mkdir(sizes[i]["dirName"])
            image.save(os.path.join(sizes[i]["dirName"], iconName))
            if type == 'launcher':
                image.save(os.path.join(sizes[i]["dirName"], roundIconName))
        logger.info("Done making icons.")
    except:
       logger.error("Failed to make icons!")

def main():
    if len(sys.argv) < 3:
        url = input("Please enter the URL of the desired image:\n")
        type = input("type \"launcher\" or \"notification\" for specifiying icon type\n")
    else:
        url = sys.argv[1]
        type = sys.argv[2]

    if type == 'launcher':
        sizes = ic_launcher_sizes
    else:
        sizes = ic_notification_sizes
    
    try:
        image = Image.open(url)
    except:
        logger.error("Failed to open the specified URL!")
        return
    
    # checks if the file has image extension
    if not re.search("^.*\.png|\.jpg|\.jpeg$", url):
        logger.error("Selected file is not an Image!")
    # checks if the image size is not smaller than first element of sizes array
    elif (image.size[0] < sizes[0]["values"][0] or image.size[1] < sizes[0]["values"][1]):
        logger.error("Selected image is too small. Please select an image with width and height of at least "+str(sizes[0]["values"][0])+" pixels.")
    else:
        if re.search("^.*\.jpg|\.jpeg$", url):
            logger.warning("Selected file format is a non PNG image. Concider using PNG formatted images for icons as Android documents suggest so.")
        if (image.size[0] != image.size[1]):
            logger.warning("Selected file does not have equal width and height. Concider using an square image to prevent distortion.")
        makeIcons(image, type)

main()