from app.services.llm_service import LLMService


llm = LLMService()

response = llm.generate(
    "Explain what PySpark is in 2 sentences."
)

print("\nLLM RESPONSE:")
print(response)