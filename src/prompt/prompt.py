
def get_field_detection_prompt(base64_image):
    """Prompt to detect field names from Image."""
    messages = [
        {
            "role": "system",
            "content": (
                """You are a smart document analyst trained to extract field names of bills and invoices images.
                Your task is to carefully analyze the image and return a list of all field names present in it.\n\n
                Include All the fields that are mentioned in the image
                Do not miss any fields.\n\n
                **Output Structure**:
                ```python
                [
                    "field_name1",
                    "field_name2",
                    "field_name3",
                    ...
                ]
                ```
                """
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                }
            ],
        },
    ]
    return messages


def get_field_value_extraction_prompt(base64_image, fields):
    """Prompt to extract values for given fields from Image of a bill/invoice."""
    example_json = """{
  "Sold By": "Varasiddhi Silk Exports, 75, 3rd Cross, Lalbagh Road, BENGALURU, KARNATAKA, 560027, IN",
  "PAN No": "AACFV3325K",
  "GST Registration No": "29AACFV3325K1ZY",
  "Item List": [
    {
      "sl_no": 2,
      "description": "Varasiddhi Silks Men's Formal Shirt (SH-05-40, Navy Blue, 40) | B07KGCS2X7 ( SH-05-40 )",
      "unit_price": 538.10,
      "quantity": 1,
      "net_amount": 538.10,
      "tax_rate": "2.5%",
      "tax_type": [
        {
          "type": "CGST",
          "amount": 13.45
        },
        {
          "type": "SGST",
          "amount": 13.45
        }
      ],
      "total_amount": 565.00
    }
  ]
}"""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a highly accurate information extractor.\n"
                "Given an image of a bill or invoice and a list of field names, extract the exact values for each field.\n"
                "Return the result in clean JSON format.\n"
                "Use only the information present in the image. Do not infer or hallucinate values.\n\n"
                "If the fields include line-item or table-related data (such as Description, Quantity, Unit Price, Tax, etc.),"
                " organize that information into an Item List array. Each item in this array should be a dictionary,"
                " where the keys correspond to the column names of the table.\n"
                "⚠️ If an item includes secondary charges (like 'Shipping Charges') directly beneath it,\n"
                "group those charges inside the same item dictionary — do not treat them as separate standalone items.\n\n"
                f"## Input Fields:\n```json\n{fields}\n```\n\n"
                "## Output Instructions:\n"
                "- Return a JSON object with keys matching the requested fields.\n"
                "- If any of the fields relate to a table, include them inside an `Item List`.\n"
                "- Be precise. Use only the content visible in the image.\n\n"
                "## Example Output:\n"
                "```json\n"
                f"{example_json}\n"
                "```"
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
                {
                    "type": "text",
                    "text": f"Extract values for the following fields:\n```json\n{fields}\n```",
                },
            ],
        },
    ]
    return messages


# def get_field_value_extraction_prompt(base64_image, fields):
#     """Prompt to extract values for known fields from OCR text."""
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 """You are a highly accurate information extractor.
#                 Given OCR text from a bill and a list of field names, your job is to extract the values for each field.\n\n"
#                 Return the result in clean JSON format.
#                 Use only the information present in the OCR text.

#                 **Output Structure**:
#                 ```json
#                 {{
#                 "Invoice Number": "...",
#                 "Date": "...",
#                 "Vendor Name": "...",
#                 "Total Amount": "...",
#                 "Item List": [
#                 {{
#                 "Name": "...",
#                 "Quantity": "...",
#                 "Price": "...",
#                 ...
#                 }},
#                 ...
#                 ]
#                 }}
#                 """
#             ),
#         },
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": f"data:image/png;base64,{base64_image}"},
#                 },
#                 {
#                     "type": "text",
#                     "text": f"Extract values for the following fields:\n```json\n{fields}\n```",
#                 },
#             ],
#         },
#     ]
#     return messages
