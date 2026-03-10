from graph.workflow import build_graph


def main():

    app = build_graph()

    email = {
        "sender": "Bhavesh@example.com",
        "subject": "Job Application",
        "body": "Hello, I want to apply for the job.Currently I am working as a AI engineer. I would be excited to contribute to your team and bring my skills and experience to the role. Please find attached my resume for your review.I look forward to the possibility of discussing how my background and qualifications align with the needs of your organization."
    }

    graph_png = app.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(graph_png)

    result = app.invoke({

        "email": email,
        "is_spam": None,
        "spam_reason": None,
        "email_category": None,
        "email_draft": None,
        "messages": []

    })


if __name__ == "__main__":
    main()