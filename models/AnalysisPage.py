from typing import List, Optional
from pydantic import BaseModel

class OverviewAnalysisSection(BaseModel):
    title: str
    content: str
    key_ideas: str

class PrepareSection(BaseModel):
    title: str
    content: str
    audience_questions: str


class ImproveSection(BaseModel):
    title: str
    recomendations: str
    mistakes: str

class AnalysisPage(BaseModel):
    title: Optional[str] = None
    id: str
    file_url: Optional[str] = None
    user_id: Optional[str] = None
    overview: Optional[OverviewAnalysisSection] = None
    prepare: Optional[PrepareSection] = None
    improve: Optional[ImproveSection] = None