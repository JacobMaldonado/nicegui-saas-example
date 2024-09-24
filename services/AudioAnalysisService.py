

from openai import OpenAI

class AudioAnalysisService:
    def __init__(self):
        self.client = OpenAI()
        self.transcriptions = {}

    def get_audio_transcript(self, audio_path):
        if audio_path in self.transcriptions:
            return self.transcriptions[audio_path]

        audio_file = open(audio_path, "rb")
        transcript = self.client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["segment"]
        )
        self.transcriptions[audio_path] = transcript
        return transcript.model_dump()