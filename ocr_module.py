from paddleocr import PaddleOCR

#ocr function

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, enable_mkldnn=False)

def get_ocr_text(image_path):
    result = ocr.ocr(image_path, cls=True)
    texts = []
    for line in result:
        for word in line:
            texts.append(word[1][0])
    return " ".join(texts)