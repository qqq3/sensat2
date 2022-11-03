import os
from osgeo import gdal
from PIL import Image, ImageDraw, ImageFont
import datetime

shp_clip = 'clip_polygon.shp'
input_path = 'downloaded_img/'
clipped_path = 'downloaded_img/clipped_img/'
converted_img = 'downloaded_img/converted_img/'


def get_date(element):
    return element[11:26]


img_list = [img for img in sorted(os.listdir(input_path), key=get_date) if img[-4:] == '.jp2']
num = 1
print("Clipping images ...")
for img in img_list:
    options = gdal.WarpOptions(cutlineDSName=shp_clip, cropToCutline=True)
    out_img = gdal.Warp(destNameOrDestDS='{0}{1:02d}_{2}'.format(clipped_path, num, img), srcDSOrSrcDSTab=input_path + img, options=options)
    num += 1
print("Images clipped")

img_list = [img for img in sorted(os.listdir(clipped_path)) if img[-4:] == '.jp2']
print("Converting images ...")
for img in img_list:
    out_img = gdal.Translate(destName=converted_img + img + '.jpg', srcDS=clipped_path + img, format='JPEG')
print("Images converted")

img_list = [img for img in sorted(os.listdir(converted_img)) if img[-4:] == '.jpg']
print("Saving images ...")
num = 1
for img in img_list:
    SENSING_DATE_STR = img[14:29]
    print(SENSING_DATE_STR)
    SENSING_DATE = datetime.datetime.strptime(SENSING_DATE_STR, '%Y%m%dT%H%M%S')
    opened_image = Image.open(converted_img + img)
    font = ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf', 48)
    position = (10, 10)
    text = str(SENSING_DATE.date())

    draw_text = ImageDraw.Draw(opened_image)
    left, top, right, bottom = draw_text.textbbox(position, text, font=font)
    draw_text.rectangle((left-5, top-5, right+5, bottom+5), fill=(66, 65, 77))
    draw_text.text(position, text, fill=(255, 255, 255), font=font)

    opened_image.save('{0}sensat_{1:03d}.jpg'.format(converted_img, num))
    num += 1
print("Images saved")
