from agents import OpenAIChatCompletionsModel,RunConfig,AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
# gemini_api_key = os.getenv("AIzaSyC2jnK9WxVggeWSKV1qypuDvrTefrzGG2U")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,#1
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model= OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",#2
    openai_client=external_client
)

config = RunConfig(
    model=model,#3
    model_provider=external_client,
    tracing_disabled=True)