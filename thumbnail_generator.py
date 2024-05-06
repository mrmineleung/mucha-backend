import requests
from PIL import Image


def combine_images(columns, space, images, filename):
    rows = len(images) // columns
    if len(images) % columns:
        rows += 1
    # width_max = max([Image.open(image).width for image in images])
    # height_max = max([Image.open(image).height for image in images])
    width_max = 120
    height_max = 120
    background_width = width_max*columns + (space*columns)-space
    background_height = height_max*rows + (space*rows)-space
    background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))
    x = 0
    y = 0
    for i, image in enumerate(images):
        img = Image.open(requests.get(image, stream=True).raw)
        img = img.resize((width_max, height_max))
        x_offset = int((width_max-img.width)/2)
        y_offset = int((height_max-img.height)/2)
        background.paste(img, (x+x_offset, y+y_offset))
        x += width_max + space
        if (i+1) % columns == 0:
            y += height_max + space
            x = 0
    background.save(f'thumbnail/{filename}.png')


if __name__ == '__main__':
    combine_images(columns=2, space=0, images=['https://cdnimg.melon.co.kr/cm2/album/images/114/50/069/11450069_20240325110702_500.jpg/melon/resize/120/quality/80/optimize',
                                            'https://cdnimg.melon.co.kr/cm2/album/images/114/02/655/11402655_20240129121016_500.jpg/melon/resize/120/quality/80/optimize',
                                            'https://cdnimg.melon.co.kr/cm2/album/images/114/74/894/11474894_20240426103349_500.jpg/melon/resize/120/quality/80/optimize',
                                            'https://cdnimg.melon.co.kr/cm2/album/images/113/91/902/11391902_20240122132041_500.jpg/melon/resize/120/quality/80/optimize',
                                            'https://cdnimg.melon.co.kr/cm2/album/images/114/54/681/11454681_20240328174504_500.jpg/melon/resize/120/quality/80/optimize',
                                            'https://cdnimg.melon.co.kr/cm2/album/images/114/21/941/11421941_20240220105008_500.jpg/melon/resize/120/quality/80/optimize',
                                            ], filename='image')
