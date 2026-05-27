import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

class OCRScreenHandler(object):
    def __init__(self):
        super(OCRScreenHandler, self).__init__()

        self.running = True

    def image_to_text(self, image_name, image_lang="eng", cropped=False, filtered=False, pointed=False, enhanced=False, x1=None, y1=None, x2=None, y2=None):
        img = Image.open(image_name)
        if cropped:
            img = img.convert('L')

            if enhanced:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(2)

            if pointed:
                threshold = 128
                img = img.point(lambda p: p > threshold and 255)

            if filtered:
                img = img.filter(ImageFilter.MedianFilter(3))

            # 4. Denoise using a median filter
            #img = img.filter(ImageFilter.MedianFilter(3))

            # 5. Resize the image (optional, to improve OCR accuracy)
            #img = img.resize((img.width * 2, img.height * 2))  # Double the size

            #x1, y1, x2, y2 = 874, 260, 1219, 323

            # Crop the image to the specified region
            cropped_img = img.crop((x1, y1, x2, y2))
            #cropped_img.save('cropped_image.png') # Saves secondary image
            return pytesseract.image_to_string(cropped_img, lang=image_lang)
        return pytesseract.image_to_string(img, lang=image_lang)
    
