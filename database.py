"""SQLAlchemy 엔진 설정 및 DB 세션(get_db) 의존성 관리."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 데이터베이스 접속 주소(SQLite 파일 경로)
SQLALCHEMY_DATABASE_URL = "sqlite:///./stocksync.db"

# 2. 커넥션 풀 및 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # 충돌 방지 락을 풀고 요청 간 세션 공유를 허용
    connect_args={"check_same_thread": False}
)

# 3. 데이터베이스 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. ORM 모델들이 상속받을 기본 클래스
Base = declarative_base()

# 5. FastAPI 요청 시 DB 세션을 열고 닫아주는 의존성(Dependency) 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()