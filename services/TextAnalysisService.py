from openai import OpenAI

class TextAnalysisService:
    def __init__(self):
        self.client = OpenAI()

    def analyze(self, text, prompt, length = None):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a LLM that receives an instruction and perform it as it is instructed."},
                {"role": "user", "content": f"with this text as a context '{text}' perform this: {prompt}"}
            ],
            max_tokens=length
        )
        return completion.choices[0].message.content