from langchain_core.prompts import ChatPromptTemplate

HISTORY_PROMPT = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert assistant that rewrites follow-up questions.

Your task is to convert the user's latest question into a
standalone question using the previous conversation.

Rules:

1. Preserve the original meaning.
2. Replace pronouns like:
   - it
   - they
   - this
   - that
   - these
   - those

   with the correct subject from the conversation.

3. Do NOT answer the question.

4. Return ONLY the rewritten standalone question.

If the question is already standalone,
return it unchanged.
"""
        ),

        (
            "human",
            """
Conversation:

{history}

Current Question:

{question}
"""
        ),
    ]
)