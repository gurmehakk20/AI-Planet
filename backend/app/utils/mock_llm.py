def get_mock_llm_response(query, context=None):
    """
    Returns a static or slightly dynamic response for testing the workflow.
    """
    if context:
        return f"[Mock LLM] Based on context: {context[:50]}... Answer to '{query}'"
    return f"[Mock LLM] Answer to '{query}'"
