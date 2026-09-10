from app.classification.topic_classifier import TopicClassifier


classifier = TopicClassifier(
    "data/curriculum.json"
)

question = """
Can you explain what "Catalyst Optimizer" is in Spark
and how it contributes to PySpark's performance?
"""

answer = """
The Catalyst Optimizer is a Spark SQL query optimization
framework. It takes the logical operations defined through
DataFrames or Spark SQL, analyzes them, applies optimization
rules, and produces an efficient physical execution plan.
"""

result = classifier.classify(
    question,
    answer
)

print("\nCLASSIFICATION RESULT:")
print(result)