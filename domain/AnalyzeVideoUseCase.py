
from models.AnalysisPage import AnalysisPage, ImproveSection, OverviewAnalysisSection, PrepareSection
from services.AnalysisRepository import AnalysisRepository
from services.AudioAnalysisService import AudioAnalysisService
from services.TextAnalysisService import TextAnalysisService


class AnalyzeVideoUseCase:
    def __init__(self):
        self.audio_analysis_service = AudioAnalysisService()
        self.text_analysis_service = TextAnalysisService()
        self.analysis_repository = AnalysisRepository()

    def analyze_main_idea(self, video_path, id):
        transcript = self.audio_analysis_service.get_audio_transcript(video_path)
        overview_text =  self.text_analysis_service.analyze(transcript['text'], "get a summary in 3 sentences")
        key_ideas_text = self.text_analysis_service.analyze(transcript['text'], "get 5 or less key ideas as a bullet list in markdown")
        self.analysis_repository.update_analysis(AnalysisPage(id=id, overview=OverviewAnalysisSection(title="Overview", content=overview_text, key_ideas=key_ideas_text)))
        return {"overview": overview_text, "key_ideas": key_ideas_text}
    
    def analyze_questions(self, video_path, id):
        transcript = self.audio_analysis_service.get_audio_transcript(video_path)
        instruction = """generate 5 questions that the audience may have, don't answer them, just generate the questions. keep them simple."""
        questions_text = self.text_analysis_service.analyze(transcript['text'], instruction)
        instruction_audience = """Answer shortly this questions about the audience based on the text, guess them based on the context.
        - Why is your audience here?
        - What are their expectations?
        - What are their motivations?
        - What do they want to know?
        - What will keep them engaged?
        """ 
        audience_questions_text = self.text_analysis_service.analyze(transcript['text'], instruction_audience)
        self.analysis_repository.update_analysis(AnalysisPage(id=id, prepare=PrepareSection(title="Questions", content=questions_text, audience_questions=audience_questions_text)))
        
        return {"questions": questions_text, "audience_questions": audience_questions_text}
    
    def improve_transcript(self, video_path, id, length=100):
        transcript = self.audio_analysis_service.get_audio_transcript(video_path)
        instruction_mistakes = """
        Act as a LLM function that gets as input a presentation text and returns possible mistakes on the presentation structure. Take into consideration this possible mistakes
        - make it concrete
        - avoid Take a really long time to explain what your talk is about
        - Split them in small parts
        - Expand the questions before answering
        - Simplify Complex Ideas
        - Avoid being too technical 
        - Engage with the Audience
        Place 5 mistakes in a markdown list with a recomendation on how to fix it. do not answer anything else and do not include a title.
        Each one should contain:
        - Mistake
        - Current Text that contains the mistake (if possible)
        - Recomendation
        """
        instruction = """
        Act as a LLM function that gets as input one presentation transcript and returns suggestions based on the text, taking into consideration the following points.
        - How to Start the presentation in a more engaging way
        - example of a story that connects with the audience
        - Recomendations to Engage with the Audience in this topic
        - How to End on a more serious tone, and Add a reflection at the very end.
        Output each one as a markdown list, do not use titles, use bold instead.
        """
        mistakes = self.text_analysis_service.analyze(transcript['text'], instruction_mistakes)
        recomendations = self.text_analysis_service.analyze(transcript['text'], instruction)
        self.analysis_repository.update_analysis(AnalysisPage(id=id, improve=ImproveSection(title="Improve", mistakes=mistakes, recomendations=recomendations)))
        return {"mistakes": mistakes, "recomendations": recomendations}
    
    def get_analysis(self, id):
        return self.analysis_repository.get_analysis_by_id(id)