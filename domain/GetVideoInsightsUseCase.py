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
        import os
        import re
        
        if len(upload_file.file) > 1024 * 1024 * 25:
            raise Exception("File size too large, upload a shorter file")
        
        # Sanitize file extension to prevent path traversal
        file_extension = upload_file.file_name.split(".")[-1]
        # Only allow alphanumeric extensions
        if not re.match(r'^[a-zA-Z0-9]+$', file_extension):
            raise Exception("Invalid file extension")
        
        # Ensure audios directory exists
        os.makedirs('./audios', exist_ok=True)
        
        audio_id = str(uuid.uuid4())
        audio_path = os.path.abspath(f'./audios/{audio_id}.mp3')
        
        # Verify the path is within the audios directory (prevent path traversal)
        if not audio_path.startswith(os.path.abspath('./audios')):
            raise Exception("Invalid file path")
        
        if "video" in upload_file.type:
            video_path = os.path.abspath(f'./video.{file_extension}')
            with open(video_path, 'wb') as f:
                f.write(upload_file.file)
            video_file_clip = VideoFileClip(video_path)
            audio = video_file_clip.audio
            audio.write_audiofile(audio_path)
            with open(audio_path, 'rb') as f:
                result = self.file_storage_service.save(f"{audio_id}.mp3", f.read())
            # Clean up video file
            try:
                os.remove(video_path)
            except Exception:
                pass
        else:
            result = self.file_storage_service.save(f"{audio_id}.mp3", upload_file.file)
            with open(audio_path, 'wb') as f:
                f.write(upload_file.file)
        
        audio = AudioSegment.from_file(audio_path)
        duration_seconds = len(audio) / 1000.0  # pydub calculates in milliseconds
        print(f"Duration: {duration_seconds:.2f} seconds")
        if plan != 'paid' and duration_seconds > 120:
            raise Exception("2 minutes limit for free users")
        elif plan == 'paid' and duration_seconds > 1800:
            raise Exception("30 minutes limit for paid users")
        self.analysis_repository.create_analysis(AnalysisPage(id=audio_id, title=upload_file.file_name, file_url=result, user_id="1"))
        return audio_id