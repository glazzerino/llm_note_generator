from abc import ABC, abstractmethod
from dotenv import load_dotenv
import openai
import os
import logging
from prompts import return_summarization_prompt

load_dotenv()

token = os.getenv("TOKEN")
model = os.getenv("MODEL")
llm_server = os.getenv("LLM_SERVER")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

client = openai.OpenAI(base_url="http://localhost:8080/v1", api_key=token)


def chat_inference(model, prompt):
    messages = [{"role": "user", "content": prompt}]
    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=500,
    )

    return chat_completion.choices[0].message.content


class Processor(ABC):
    @abstractmethod
    def process_transcription(self, data):
        pass


class PresentationTranscriptProcessor(Processor):
    """Processes a list of text that represent the slides in a presentation.
    An LLM is used to synthethize the text and return a summary of the presentation on a per-slide basis.

    Schema for the data must be a json list of strings:

    {
    "transcriptions": [
        "The first transcription text goes here.",
        "Here is the second transcription text.",
        "This is the third example of a transcription."
        ]
    }
    """

    def __init__(self):
        self.context = ""
        self.synthesis = []

    def llm_summarize(self, text):
        prompt = return_summarization_prompt(text)
        return chat_inference(model, prompt)

    def llm_generate_context(self, text) -> str:
        prompt = f"""Given the following text, return a list of keywords that best capture the context of it.
            Text: {text}
        """
        logging.info(f"Generating context for text: {text}")
        return chat_inference(model, prompt)

    def process_transcription(self, transcription_list: list):
        transcription_list = transcription_list[
            ::-1
        ]  # Reverse the list so that the first slide is processed first
        for text in transcription_list:
            slide_synthesis = self.llm_summarize(text)
            self.synthesis.append(slide_synthesis)
            save(slide_synthesis)
            logging.info(f"Slide synthesis: {slide_synthesis}")

        return self.synthesis


def save(sythesis: str):
    # Append newly generated text to synthesis.md file
    with open("paleochristian.md", "a") as f:
        f.write(sythesis)
        f.write("\n\n")
        logging.info("Slide synthesis appended to synthesis.md")
