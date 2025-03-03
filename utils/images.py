from PIL import Image
import base64
import io


def sizeCap(dataURI, size=2e6):
    """
    This function takes a data URI and a maximum size (in bytes) as input.
    It decodes the data URI into an image and checks if the image is within the minimum size
    If not, it uses an appropriate Python library to compress the image and return a new data URI
    """
    # Extract the base64 encoded data from the URI
    header, encoded = dataURI.split(",", 1)

    # Decode the base64 data
    binary_data = base64.b64decode(encoded)

    # Create a bytes buffer from the decoded data
    image_buffer = io.BytesIO(binary_data)

    # Open the image using PIL
    img = Image.open(image_buffer)

    # Convert to RGB if image is in RGBA mode
    if img.mode == "RGBA":
        img = img.convert("RGB")

    # Check current size
    current_buffer = io.BytesIO()
    img.save(current_buffer, format="JPEG", quality=95)
    current_size = len(current_buffer.getvalue())

    if current_size <= size:
        return dataURI

    # If image is larger than target size, compress it
    quality = 95
    output_buffer = io.BytesIO()

    while quality > 5:
        output_buffer.seek(0)
        output_buffer.truncate()
        img.save(output_buffer, format="JPEG", quality=quality)
        if len(output_buffer.getvalue()) <= size:
            break
        quality -= 5

    # Convert back to base64 data URI
    compressed_data = base64.b64encode(output_buffer.getvalue()).decode()
    mime_type = header.split(":")[1].split(";")[0]
    new_data_uri = f"data:{mime_type};base64,{compressed_data}"

    return new_data_uri
