"""
This module provides utilities for working with various language models
and embeddings.

It includes functions for setting up Azure OpenAI models, and manages
API key retrieval.
"""

import os
# from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain_huggingface import ChatHuggingFace
# from langchain_community.llms import HuggingFaceHub  # Correct import


load_dotenv()


# def _get_azure_openai_model(deployment_name):
#     """
#     Initialize and configure the Azure OpenAI model.

#     Returns:
#         AzureChatOpenAI: Configured Azure OpenAI language model.
#     """
#     if not all(
#         os.getenv(var)
#         for var in [
#             "AZURE_OPENAI_API_KEY",
#             "OPENAI_GPT_4O_API_VERSION",
#             "AZURE_OPENAI_ENDPOINT",
#         ]
#     ):
#         raise ValueError(
#             "Azure OpenAI API is not set in the environment variables: "
#             "'AZURE_OPENAI_API_KEY', 'OPENAI_GPT_4O_API_VERSION', 'AZURE_OPENAI_ENDPOINT'."
#         )
#     llm = AzureChatOpenAI(
#         azure_deployment=deployment_name,
#         api_version=os.getenv("OPENAI_GPT_4O_API_VERSION"),
#     )
#     return llm


def _get_openai_model(model_name):
    """
    Initialize and configure the OpenAI model.

    Returns:
        ChatOpenAI: Configured OpenAI language model.
    """
    api_token = os.getenv("OPENAI_API_KEY")
    if not api_token:
        raise ValueError(
            "OPEN AI API is not set in the environment variable 'OPENAI_API_KEY'."
        )
    llm = ChatOpenAI(model=model_name, openai_api_key=api_token)
    return llm


# def _get_hugging_face_model(model_name):
#     """
#     Initialize and configure the Hugging Face model.
#     """
#     # Ensure the Hugging Face API token is set in the environment variables
#     api_token = os.getenv("HUGGING_FACE_API")
#     if not api_token:
#         raise ValueError(
#             "Hugging Face API token is not set in the environment variable 'HUGGING_FACE_API'."
#         )
#     hf_model = HuggingFaceHub(
#         repo_id=model_name,
#         task="text-generation",  # Change this based on your model
#         huggingfacehub_api_token=api_token,
#     )

#     llm = ChatHuggingFace(llm=hf_model)
#     return llm


def get_llm_model(vendor="", model_name=""):
    """
    Select and return the specified language model.
    Currently supports Azure OpenAI models.
    """
    print(model_name)
    # if vendor == "azure":
    #     llm = _get_azure_openai_model(model_name)
    #     return llm
    if vendor == "openai":
        return _get_openai_model(model_name)

    # if vendor == "hugging_face":
    #     return _get_hugging_face_model(model_name)
    return None
