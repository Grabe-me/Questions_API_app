from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class ResultData(BaseModel):
    id: int = Field()
    question: str = Field()
    answer: str = Field()
    created_at: datetime = Field()


class ResponseData(BaseModel):
    status: int
    msg: str
    data: List[ResultData]


class QuestionNum(BaseModel):
    question_num: int = Field(gt=0)
