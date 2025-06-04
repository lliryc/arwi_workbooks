import uvicorn
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Header
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, CustomWorkbook
from pydantic import BaseModel
import dotenv
import os
import requests

dotenv.load_dotenv()

# Authentication configuration
AUTH_VALIDATE_URL = "https://arwi.mbzuai.ac.ae/account/email_auth/validate-token"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

arwi_app = FastAPI()
router = APIRouter(prefix="/custom_workbooks")


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency for token validation
async def validate_token(
    authorization: str = Header(..., description="Bearer token")
) -> str:
    """
    # TODO: Uncomment this when the token validation is implemented
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = authorization.replace("Bearer ", "")
    response = requests.get(f"{AUTH_VALIDATE_URL}?token={token}")

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    """
    return True


# Pydantic models for request/response
class CustomWorkbookBase(BaseModel):
    task_level: str
    title: str
    prompt: str
    img_url: str
    essay: str
    min_words: int
    labels: List[str]
    user_id: str


class CustomWorkbookCreate(CustomWorkbookBase):
    pass


class CustomWorkbookResponse(CustomWorkbookBase):
    workbook_id: str
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=CustomWorkbookResponse)
def create_workbook(
    workbook: CustomWorkbookCreate,
    db: Session = Depends(get_db),
    # success_auth: str = Depends(validate_token)
):
    db_workbook = CustomWorkbook(**workbook.model_dump())
    db.add(db_workbook)
    db.commit()
    db.refresh(db_workbook)
    return db_workbook


@router.get("/", response_model=List[CustomWorkbookResponse])
def list_workbooks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # success_auth: str = Depends(validate_token)
):
    workbooks = db.query(CustomWorkbook).offset(skip).limit(limit).all()
    return workbooks


@router.get("/{workbook_id}", response_model=CustomWorkbookResponse)
def get_workbook(
    workbook_id: str,
    db: Session = Depends(get_db),
    # success_auth: str = Depends(validate_token)
):
    workbook = (
        db.query(CustomWorkbook)
        .filter(CustomWorkbook.workbook_id == workbook_id)
        .first()
    )
    if workbook is None:
        raise HTTPException(status_code=404, detail="Workbook not found")
    return workbook


@router.put("/{workbook_id}", response_model=CustomWorkbookResponse)
def update_workbook(
    workbook_id: str,
    workbook: CustomWorkbookCreate,
    db: Session = Depends(get_db),
    # success_auth: str = Depends(validate_token)
):
    db_workbook = (
        db.query(CustomWorkbook)
        .filter(CustomWorkbook.workbook_id == workbook_id)
        .first()
    )
    if db_workbook is None:
        raise HTTPException(status_code=404, detail="Workbook not found")

    for key, value in workbook.model_dump().items():
        setattr(db_workbook, key, value)

    db.commit()
    db.refresh(db_workbook)
    return db_workbook


@router.delete("/{workbook_id}")
def delete_workbook(
    workbook_id: str,
    db: Session = Depends(get_db),
    # success_auth: str = Depends(validate_token)
):
    db_workbook = (
        db.query(CustomWorkbook)
        .filter(CustomWorkbook.workbook_id == workbook_id)
        .first()
    )
    if db_workbook is None:
        raise HTTPException(status_code=404, detail="Workbook not found")

    db.delete(db_workbook)
    db.commit()
    return {"message": "Workbook deleted successfully"}


# Include router in the main app
arwi_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(arwi_app, host="0.0.0.0", port=9995)
