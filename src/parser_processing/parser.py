from src.prompt.prompt import (
    get_field_detection_prompt,
    get_field_value_extraction_prompt,
)

from src.model.model import get_llm_model
from src.utils import extract_and_parse_json  # , encode_image


def extract_fields_from_bill(base64_image, model_name="gpt-4o"):
    field_details = extract_field(base64_image, model_name)
    field_from_bill = extract_field_values(base64_image, field_details, model_name)
    return field_from_bill


def extract_field(image, model_name):
    message = get_field_detection_prompt(image)
    llm = get_llm_model(vendor="openai", model_name=model_name)
    ai_message = llm.invoke(message)
    result_string = ai_message.content.replace("```python", "").replace("`", "")
    return result_string


def extract_field_values(image, fields, model_name):
    message = get_field_value_extraction_prompt(image, fields)
    llm = get_llm_model(vendor="openai", model_name=model_name)
    ai_message = llm.invoke(message)
    result_string = ai_message.content.replace("```json", "").replace("`", "")
    parsed_data = extract_and_parse_json(result_string)
    return parsed_data


# if __name__ == "__main__":
#     image_path = r"data\image.png"
#     extracted_image = encode_image(image_path)
#     model_name = "gpt-4o"
#     result = extract_fields_from_bill(extracted_image, model_name)
#     print(result)
