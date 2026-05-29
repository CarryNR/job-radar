from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import InterviewPost
from app.schemas import (
    DashboardStats,
    InterviewCreate,
    InterviewItem,
    InterviewListResponse,
    JobDetail,
    JobListResponse,
)
from app.services import get_dashboard_stats, get_job, list_interviews, list_jobs, sanitize_contact

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/stats", response_model=DashboardStats)
async def stats(db: AsyncSession = Depends(get_db)):
    return await get_dashboard_stats(db)


@router.get("/jobs", response_model=JobListResponse)
async def jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    city: str | None = None,
    company: str | None = None,
    keyword: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    items, total = await list_jobs(db, page=page, page_size=page_size, city=city, company_slug=company, keyword=keyword)
    return JobListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/jobs/{job_id}", response_model=JobDetail)
async def job_detail(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return job


@router.get("/interviews", response_model=InterviewListResponse)
async def interviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    items, total = await list_interviews(db, page=page, page_size=page_size)
    return InterviewListResponse(items=items, total=total, page=page, page_size=page_size)


@router.post("/interviews", response_model=InterviewItem, status_code=201)
async def create_interview(payload: InterviewCreate, db: AsyncSession = Depends(get_db)):
    if not payload.company_id and not payload.company_name:
        raise HTTPException(status_code=400, detail="请填写公司名称")

    post = InterviewPost(
        company_id=payload.company_id,
        company_name=payload.company_name,
        position=payload.position,
        rounds=payload.rounds,
        difficulty=payload.difficulty,
        content=sanitize_contact(payload.content),
        questions=payload.questions,
        author_name=payload.author_name or "匿名",
        status="pending",
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return InterviewItem.model_validate(post)
