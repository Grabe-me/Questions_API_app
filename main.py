from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models.models import columns
from schemas import ResponseData, QuestionNum
from utils import get_last_query, validated_data, upload_data


app = FastAPI(title='BeWise')


@app.post("/question", response_model=ResponseData)
async def get_questions(
        question_num: QuestionNum, session: AsyncSession = Depends(get_async_session)
) -> list[dict]:
    try:
        num = question_num.question_num
        res, query_num = await get_last_query(session)
        data_dict = await validated_data(num, query_num, session)
        if data_dict:
            await upload_data(data_dict, session)
        res = [{k: v for k, v in i.items() if k != columns[-1]} for i in res]

        return {"status": 200, "msg": "Previous query", "data": res}

    except Exception as ex:
        print(f"ERROR[func:'get_question']: {ex}")

        return {"status": 500, "msg": "Internal error. Try again later."}
