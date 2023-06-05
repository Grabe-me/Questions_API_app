from sqlalchemy import MetaData, Integer, Table, Column, String, TIMESTAMP

columns = [
    "id",
    "question",
    "answer",
    "created_at",
    "query_num"
]

metadata = MetaData()

question = Table(
    "question",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("question", String, nullable=False),
    Column("answer", String, nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("query_num", Integer, nullable=False),
)
