from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from web.config.logging_config import configure_logging
import logging

# 配置日志
configure_logging()
logger = logging.getLogger(__name__)

# 配置数据库连接字符串
DATABASE_URL = "mysql+pymysql://username:password@localhost/dbname"

# 创建 SQLAlchemy 引擎并启用连接池
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 连接池溢出数
    pool_timeout=30,  # 超时30秒
    pool_recycle=3600  # 每小时回收连接
)

# 创建 Session 类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型类
Base = declarative_base()

# 示例：定义一个 User 表
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# 创建表
Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 示例：在数据库中插入数据
def create_user(db, name: str, email: str):
    db_user = User(name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 示例：查询用户
def get_user(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# 测试连接池管理功能
if __name__ == "__main__":
    db = next(get_db())  # 获取数据库连接
    user = create_user(db, name="John Doe", email="john.doe@example.com")
    logger.info(f"Created user: {user.name} with email {user.email}")
    fetched_user = get_user(db, user_id=user.id)
    logger.info(f"Fetched user: {fetched_user.name} with email {fetched_user.email}")
