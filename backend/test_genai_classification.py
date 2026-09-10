from app.classification.topic_classifier import TopicClassifier


classifier = TopicClassifier(
    "data/curriculum.json"
)

question = "Why do we need chunking in RAG?"

answer = (
    "Because embedding models and LLMs have a limited context window, "
    "we can't feed an entire document in at once. Chunking splits the "
    "document into smaller pieces so each piece can be embedded and "
    "retrieved independently, which also improves retrieval precision "
    "since a smaller chunk is more likely to be specifically relevant "
    "to the query instead of being diluted by unrelated content."
)

result = classifier.classify(
    question,
    answer
)

print("\nCLASSIFICATION RESULT:")
print(result)
