from moviepy.editor import *
import uuid

from models.AnalysisPage import AnalysisPage
from services.AnalysisRepository import AnalysisRepository
from services.FileStorageService import FileStorageService
from pydub import AudioSegment

class GetVideoInsightsUseCase:
    def __init__(self):
        self.analysis_repository = AnalysisRepository()
        self.file_storage_service = FileStorageService()

    def execute(self, upload_file, plan):
        if len(upload_file.file) > 1024 * 1024 * 25:
            raise Exception("File size too large, upload a shorter file")
        file_extension = upload_file.file_name.split(".")[-1]
        if "video" in upload_file.type:
            with open(f'video.{file_extension}', 'wb') as f:
                f.write(upload_file.file)
            video_file_clip = VideoFileClip("./video.mp4")
            audio = video_file_clip.audio
            audio_id = str(uuid.uuid4())
            audio.write_audiofile(f"./audios/{audio_id}.mp3")
            with open(f'./audios/{audio_id}.mp3', 'rb') as f:
                result = self.file_storage_service.save(f"{audio_id}.mp3", f.read())
        else:
            audio_id = str(uuid.uuid4())
            result = self.file_storage_service.save(f"{audio_id}.mp3", upload_file.file)
            with open(f'./audios/{audio_id}.mp3', 'wb') as f:
                f.write(upload_file.file)
        audio = AudioSegment.from_file(f'./audios/{audio_id}.mp3')
        duration_seconds = len(audio) / 1000.0  # pydub calculates in milliseconds
        print(f"Duration: {duration_seconds:.2f} seconds")
        if plan != 'paid' and duration_seconds > 120:
            raise Exception("2 minutes limit for free users")
        elif plan == 'paid' and duration_seconds > 1800:
            raise Exception("30 minutes limit for paid users")
        self.analysis_repository.create_analysis(AnalysisPage(id=audio_id, title=upload_file.file_name, file_url=result, user_id="1"))
        return audio_id