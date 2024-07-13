def get_image_base64(image_path):
    import base64
    from PIL import Image
    from io import BytesIO
    image = Image.open(image_path)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
