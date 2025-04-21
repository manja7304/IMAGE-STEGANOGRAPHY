import numpy as np
from PIL import Image


def bits_provider(message):
    """Convert text (chars) to bits"""
    for char in message:
        ascii_value = ord(char)
        for power in range(7, -1, -1):
            yield (ascii_value >> power) & 1  # Extract each bit


def create_image(message, path) -> None:
    """Hide text message in image"""

    bits_in_msg = len(message) * 8
    img = Image.open(path)
    image_width, image_height = img.size
    image_size = image_width * image_height
    assert image_size >= bits_in_msg, "Image is too small or message is too long."

    pixels = np.array(img, dtype=np.uint8)

    # Clear last bit of 'Red' channel
    pixels[:, :, 0] &= 0b11111110  # Ensures all values remain within uint8

    # Save text bits in the last bit of 'Red' value
    for i, bit in enumerate(bits_provider(message)):
        row = i // image_width
        col = i % image_width
        pixels[row, col, 0] |= bit  # Set LSB

    # Save the modified image
    img = Image.fromarray(pixels)
    img.save(path)
    img.close()


def decode_image(path):
    """Decode hidden text from image"""

    img = Image.open(path)
    pixels = np.array(img, dtype=np.uint8)
    image_width, image_height = img.size

    bits = []
    for i in range(image_height):
        for j in range(image_width):
            bits.append(pixels[i, j, 0] & 1)  # Extract LSB

    bytes_l = [
        int("".join(map(str, bits[i : i + 8])), 2) for i in range(0, len(bits), 8)
    ]
    decoded_message = "".join(map(chr, bytes_l))
    print(decoded_message)
    img.close()

    return decoded_message.strip("\x00")  # Remove extra null characters

