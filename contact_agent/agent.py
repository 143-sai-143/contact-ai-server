from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    name="contact_agent",

    model=LiteLlm(model="ollama_chat/gemma3:4b"),

    description="AI assistant",

    instruction="""
You are a helpful assistant.

- If user asks general questions → answer normally
- If user asks about contacts → guide them

DO NOT execute actions.
""",

    tools=[]
)