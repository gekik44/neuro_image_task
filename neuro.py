from functools import lru_cache
import os


import tensorflow as tf
import tensorflow_hub as hub


def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image


@lru_cache(maxsize=None)
def load_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
    """Loads and preprocesses images."""
    # Cache image file locally.
    image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = tf.io.decode_image(
        tf.io.read_file(image_path),
        channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

@lru_cache(maxsize=None)
def load_local_image(my_image, image_size=(256, 256), preserve_aspect_ratio=True):
    full_path = os.path.abspath("./" + my_image)
    data_dir = tf.keras.utils.get_file(os.path.basename(full_path)[-128:], r'file:\\' + full_path)
    img = tf.io.decode_image(
        tf.io.read_file(data_dir),
        channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img


def convert_image(image_content, image_style):
    #content_image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Golden_Gate_Bridge_from_Battery_Spencer.jpg/640px-Golden_Gate_Bridge_from_Battery_Spencer.jpg'
    #content_image_url = "https://img.championat.com/s/735x490/news/big/p/y/devushki-v-muzhskom-sporte_15711590042025587306.jpg"
    content_image_url = f'static/img/{image_content}'
    style_image_url = f'static/img/{image_style}'

    output_image_size = 384
    content_img_size = (output_image_size, output_image_size)
    style_img_size = (256, 256)  # Recommended to keep it at 256.

    content_image = load_local_image(content_image_url, content_img_size)
    style_image = load_local_image(style_image_url, style_img_size)
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')

    hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    hub_module = hub.load(hub_handle)

    outputs = hub_module(content_image, style_image)
    stylized_image = outputs[0]

    tf.keras.preprocessing.image.save_img('static/img/file.png', stylized_image[0])
