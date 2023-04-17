import tensorflow as tf


STYLE_PREDICT_PATH = tf.keras.utils.get_file('style_predict.tflite', 'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite')
STYLE_TRANSFORM_PATH = tf.keras.utils.get_file('style_transform.tflite', 'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite')


# Function to load an image from a file, and add a batch dimension.
def load_image(path_to_image):
    image = tf.io.read_file(path_to_image)
    image = tf.io.decode_image(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = image[tf.newaxis, :]
    return image


# Function to pre-process by resizing an central cropping it.
def preprocess_image(image, target_dim):
    # Resize the image so that the shorter dimension becomes 256px.
    shape = tf.cast(tf.shape(image)[1:-1], tf.float32)
    short_dim = min(shape)
    scale = target_dim / short_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    image = tf.image.resize(image, new_shape)
    # Central crop the image.
    image = tf.image.resize_with_crop_or_pad(image, target_dim, target_dim)
    return image


# Function to run style prediction on preprocessed style image.
def run_style_predict(preprocessed_style_image):
    # Load the model.
    interpreter = tf.lite.Interpreter(model_path=STYLE_PREDICT_PATH)
    # Set model input.
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]["index"], preprocessed_style_image)
    # Calculate style bottleneck.
    interpreter.invoke()
    style_bottleneck = interpreter.tensor(interpreter.get_output_details()[0]["index"])()

    return style_bottleneck


# Run style transform on preprocessed style image
def run_style_transform(style_bottleneck, preprocessed_content_image):
    # Load the model.
    interpreter = tf.lite.Interpreter(model_path=STYLE_TRANSFORM_PATH)
    # Set model input.
    input_details = interpreter.get_input_details()
    interpreter.allocate_tensors()
    # Set model inputs.
    interpreter.set_tensor(input_details[0]["index"], preprocessed_content_image)
    interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
    interpreter.invoke()
    # Transform content image.
    stylized_image = interpreter.tensor(interpreter.get_output_details()[0]["index"])()
    return stylized_image


def convert_image(image_content, image_style, content_blending_ratio=0.5):
    # content_blending_ratio
    # @param {type:"slider", min:0, max:1, step:0.01}
    # Define content blending ratio between [0..1].
    # 0.0: 0% style extracts from content image.
    # 1.0: 100% style extracted from content image.

    # content_path = tf.keras.utils.get_file('belfry.jpg', 'https://storage.googleapis.com/khanhlvg-public.appspot.com/arbitrary-style-transfer/belfry-2611573_1280.jpg')
    # style_path = tf.keras.utils.get_file('style23.jpg', 'https://storage.googleapis.com/khanhlvg-public.appspot.com/arbitrary-style-transfer/style23.jpg')
    content_path = f'static/img/{image_content}'
    style_path = f'static/img/{image_style}'

    # Load the input images.
    content_image = load_image(content_path)
    style_image = load_image(style_path)

    # Preprocess the input images.
    preprocessed_content_image = preprocess_image(content_image, 384)
    preprocessed_style_image = preprocess_image(style_image, 256)

    # Calculate style bottleneck for the preprocessed style image.
    style_bottleneck = run_style_predict(preprocessed_style_image)
    # Calculate style bottleneck of the content image.
    style_bottleneck_content = run_style_predict(preprocess_image(content_image, 256))

    # Blend the style bottleneck of style image and content image
    style_bottleneck_blended = content_blending_ratio * style_bottleneck_content + (1 - content_blending_ratio) * style_bottleneck

    # Stylize the content image using the style bottleneck.
    stylized_image_blended = run_style_transform(style_bottleneck_blended, preprocessed_content_image)

    if len(stylized_image_blended.shape) > 3:
        stylized_image_blended = tf.squeeze(stylized_image_blended, axis=0)
    tf.keras.preprocessing.image.save_img('static/img/file.png', stylized_image_blended)
