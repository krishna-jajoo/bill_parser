import json
import re
import base64
from io import BytesIO
from PIL import Image


def encode_image(image_path):
    """Encode image to base64 string."""
    image = Image.open(image_path)
    buffer = BytesIO()
    image.save(buffer, format=image.format if image.format else "PNG")
    base64_encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_encoded_image


def extract_and_parse_json(response):
    """
    Extracts JSON from a response and parses it.
    """
    # Extract JSON using regex (handles extra text issues)
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        json_str = match.group(0).strip()  # Extract only JSON part
        try:
            return json.loads(json_str)  # Parse JSON
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: {e}\nFailed Response: {json_str}")
            return response
    else:
        print(f"Failed to extract JSON from response: {response}")
        return response
