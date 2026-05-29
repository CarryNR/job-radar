from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import InterviewPost
from app.schemas import InterviewItem

router = APIRouter(prefix="/admin", tags=["admin"])


def verify_admin(x_admin_token: str = Header(...)):
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=403, detail="无效的管理员 Token")


@router.get("/interviews/pending", response_model=list[InterviewItem])
async def pending_interviews(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin),
):
    result = await db.execute(
        select(InterviewPost).where(InterviewPost.status == "pending").order_by(InterviewPost.created_at.desc())
    )
    return [InterviewItem.model_validate(i) for i in result.scalars().all()]


@router.patch("/interviews/{interview_id}/approve", response_model=InterviewItem)
async def approve_interview(
    interview_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin),
):
    post = await db.get(InterviewPost, interview_id)
    if not post:
        raise HTTPException(status_code=404, detail="面经不存在")
    post.status = "approved"
    await db.commit()
    await db.refresh(post)
    return InterviewItem.model_validate(post)


@router.patch("/interviews/{interview_id}/reject", response_model=InterviewItem)
async def reject_interview(
    interview_id: int,
    reason: str = Query(default=""),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin),
):
    post = await db.get(InterviewPost, interview_id)
    if not post:
        raise HTTPException(status_code=404, detail="面经不存在")
    post.status = "rejected"
    if reason:
        post.content = f"{post.content}\n\n[审核备注: {reason}]"
    await db.commit()
    await db.refresh(post)
    return InterviewItem.model_validate(post)
