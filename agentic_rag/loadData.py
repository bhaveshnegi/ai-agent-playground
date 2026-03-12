import datasets
from llama_index.core.schema import Document

# Load the dataset
guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

# Convert dataset entries into Document objects
# docs = [
#     Document(
#         text="\n".join([
#             f"Name: {guest_dataset['name'][i]}",
#             f"Relation: {guest_dataset['relation'][i]}",
#             f"Description: {guest_dataset['description'][i]}",
#             f"Email: {guest_dataset['email'][i]}"
#         ]),
#         metadata={"name": guest_dataset['name'][i]}
#     )
#     for i in range(len(guest_dataset))
# ]
docs = []
for row in guest_dataset:
    docs.append(
        Document(
            text=f"""
            Name: {row['name']}
            Relation: {row['relation']}
            Description: {row['description']}
            Email: {row['email']}
            """,
            metadata={"name": row["name"]}
        )
    )