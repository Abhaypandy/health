def generate_answer(query: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)

    prompt = f"""
    You are a clinical assistant.
    Answer the question using ONLY the context.

    Context:
    {context}

    Question:
    {query}
    """

    # later → LLaMA / Mistral / OpenAI / Ollama
    return prompt
