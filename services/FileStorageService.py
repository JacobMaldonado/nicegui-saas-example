from google.cloud import storage

class FileStorageService:

    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket("audio-files-confidentier")

    def save(self, file_name, file):
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(file)
        return blob.public_url

    def get(self, file_name):
        blob = self.bucket.blob(file_name)
        return blob.download_as_string()