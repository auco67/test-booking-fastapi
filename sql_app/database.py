from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session

# SQLite設定
SQLITE_FILE_NAME= "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"
CONNECT_ARGS = { "check_same_thread": False }

# SQLiteエンジン設定
engine = create_engine(SQLITE_URL, connect_args=CONNECT_ARGS)

# Session依存関係の作成
def get_session():
    with Session(engine) as session:
        yield session

# SessionDependency型
SessionDep = Annotated[Session, Depends(get_session)]