from google.cloud import firestore

from models.AnalysisPage import AnalysisPage


class AnalysisRepository:
    def __init__(self):
        self.analysis = firestore.Client(project="confidentier")

    def get_analysis_by_user(self, user_id):
        return self.analysis.collection("analysis").where("user_id", "==", user_id).get()

    def get_analysis_by_id(self, analysis_id):
        return AnalysisPage.model_validate(self.analysis.collection("analysis").document(analysis_id).get().to_dict())

    def update_analysis(self, analysis: AnalysisPage):
        self.analysis.collection("analysis").document(analysis.id).update(analysis.model_dump(exclude_none=True))

    def create_analysis(self, analysis: AnalysisPage):
        self.analysis.collection("analysis").document(analysis.id).set(analysis.model_dump(exclude_none=True))