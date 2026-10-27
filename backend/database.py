import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

os.makedirs("./data/db", exist_ok=True)
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from backend.models import Base as ModelsBase, Intersection, User
    from backend.auth_utils import hash_password
    ModelsBase.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        inter = db.query(Intersection).filter(Intersection.id == settings.DEFAULT_INTERSECTION_ID).first()
        if not inter:
            default_inter = Intersection(
                id=settings.DEFAULT_INTERSECTION_ID,
                name=settings.DEFAULT_INTERSECTION_NAME,
                latitude=40.7527,
                longitude=-73.9772,
                num_lanes=4,
                status="active"
            )
            db.add(default_inter)
        
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            db_admin = User(
                username="admin",
                email="admin@traffic.ai",
                hashed_password=hash_password("admin123"),
                full_name="Traffic Operations Director",
                role="ADMIN",
                is_active=True
            )
            db.add(db_admin)
        else:
            # Update password hash to ensure valid bcrypt format
            admin.hashed_password = hash_password("admin123")
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Database init warning: {e}")
    finally:
        db.close()
