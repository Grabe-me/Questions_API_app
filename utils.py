from datetime import datetime
from select import select
from typing import List, Any

import httpx
from sqlalchemy import insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from config import url
from models.models import columns, question


async def get_request(num: int, query_num: int) -> List | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{url}{num}")
    if response.status_code == 200:
        data = response.json()
        for i in data:
            for key in list(i.keys()).copy():
                if key not in columns:
                    i.pop(key)
                if key == columns[-2]:
                    i[key] = datetime.fromisoformat(i[key].replace("Z", ""))
            i[columns[-1]] = query_num + 1

        return data
    else:

        return None


async def upload_data(data: list, session: AsyncSession) -> None:
    for value in data:
        stmt = insert(question).values(**value)
        await session.execute(stmt)
    await session.commit()


async def get_last_query(session: AsyncSession) -> tuple[list[dict[Any, Any]], Any]:
    query_num_select = await session.execute(
        select(func.max(question.c.query_num))
    )
    query_num = query_num_select.fetchone()[0]
    query = await session.execute(
        select(question).where(question.c.query_num == query_num)
    )
    result = query.all()

    if not query_num and not result:
        return [], 0

    data = [dict(zip(columns, values)) for values in result]
    return data, query_num


async def get_all_id(session: AsyncSession) -> List[int]:
    query = select(question.c.id)
    res = await session.execute(query)

    return [i[0] for i in res.all()]


async def validated_data(
        num: int, query_num: int, session: AsyncSession
) -> list[dict[Any, Any] | None]:
    uploaded_id = await get_all_id(session)
    new_query = []

    while len(new_query) <= num:
        new_questions = await get_request(num, query_num)
        if not new_questions:
            continue
        for q in new_questions:
            if _id := q.get("id") not in uploaded_id:
                new_query.append(q)
                num -= 1
                uploaded_id.append(_id)
        if num:
            await validated_data(num, query_num, session)

    return new_query
