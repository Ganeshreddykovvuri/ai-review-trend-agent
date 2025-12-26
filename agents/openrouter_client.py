from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Review Trend Agent"
    }
)
