
def return_summarization_prompt(text: str) -> str:
    return f"""
        Task: Markdown Slide Summarization

        Markdown Summarization Task

        Input Slide Text: {text}
        Direct Instruction: Create a Markdown-formatted summary.
        Note: Only the summary is required. Do not repeat the input or add extraneous comments.
        Output:
        """