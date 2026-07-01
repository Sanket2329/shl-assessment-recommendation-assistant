from pydantic import BaseModel
from typing import List


class AssessmentSchema(BaseModel):
    id: int
    name: str
    description: str

    category: str
    test_type: str

    skills: List[str]

    job_levels: List[str]

    languages: List[str]

    duration: int

    remote_testing: bool

    adaptive: bool

    url: str