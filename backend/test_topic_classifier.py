from app.classification.topic_classifier import TopicClassifier

classifier = TopicClassifier("data/curriculum.json")

topics = classifier.get_topics()

print("Total topics:", len(topics))

for topic in topics:
    print("\nTopic:", topic["topic"])
    for subtopic in topic["subtopics"]:
        print("  -", subtopic)

question = "Why do we need chunking in RAG?"
answer = (
    "Because you can't feed an entire document into the model at once, so "
    "we split it into smaller pieces before embedding them, which also makes "
    "retrieval more precise since we only pull back the relevant piece."
)

print("\n" + "=" * 80)
print("CLASSIFY TEST")
print("=" * 80)
print("Question:", question)
print("Answer:", answer)

result = classifier.classify(question, answer)

print("\nResult:", result)
