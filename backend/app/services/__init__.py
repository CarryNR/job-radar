import re
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Company, InterviewPost, JobPosting, JobSkill, Skill, SkillTrend
from app.schemas import (
    DashboardStats,
    InterviewItem,
    JobDetail,
    JobListItem,
    SkillTrendItem,
)


def sanitize_contact(text: str) -> str:
    text = re.sub(r"1[3-9]\d{9}", "[手机号已隐藏]", text)
    text = re.sub(r"[\w.-]+@[\w.-]+\.\w+", "[邮箱已隐藏]", text)
    return text


async def list_jobs(
    db: AsyncSession,
    *,
    page: int = 1,
    page_size: int = 20,
    city: str | None = None,
    company_slug: str | None = None,
    keyword: str | None = None,
) -> tuple[list[JobListItem], int]:
    query = (
        select(JobPosting)
        .join(Company)
        .where(JobPosting.is_active.is_(True))
        .options(selectinload(JobPosting.company), selectinload(JobPosting.job_skills).selectinload(JobSkill.skill))
    )

    if city:
        query = query.where(JobPosting.city == city)
    if company_slug:
        query = query.where(Company.slug == company_slug)
    if keyword:
        like = f"%{keyword}%"
        query = query.where(or_(JobPosting.title.ilike(like), JobPosting.description.ilike(like)))

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    result = await db.execute(
        query.order_by(JobPosting.crawled_at.desc()).offset((page - 1) * page_size).limit(page_size)
    )
    jobs = result.scalars().all()

    items = [
        JobListItem(
            id=j.id,
            title=j.title,
            city=j.city,
            salary_min=j.salary_min,
            salary_max=j.salary_max,
            experience=j.experience,
            source=j.source,
            source_url=j.source_url,
            crawled_at=j.crawled_at,
            company=j.company,
            skills=[js.skill.name for js in j.job_skills],
        )
        for j in jobs
    ]
    return items, total


async def get_job(db: AsyncSession, job_id: int) -> JobDetail | None:
    result = await db.execute(
        select(JobPosting)
        .where(JobPosting.id == job_id)
        .options(selectinload(JobPosting.company), selectinload(JobPosting.job_skills).selectinload(JobSkill.skill))
    )
    job = result.scalar_one_or_none()
    if not job:
        return None
    return JobDetail(
        id=job.id,
        title=job.title,
        city=job.city,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        experience=job.experience,
        source=job.source,
        source_url=job.source_url,
        crawled_at=job.crawled_at,
        company=job.company,
        skills=[js.skill.name for js in job.job_skills],
        description=job.description,
        education=job.education,
    )


async def list_interviews(
    db: AsyncSession, *, page: int = 1, page_size: int = 20, status: str = "approved"
) -> tuple[list[InterviewItem], int]:
    query = select(InterviewPost).where(InterviewPost.status == status)
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    result = await db.execute(
        query.order_by(InterviewPost.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    )
    items = [InterviewItem.model_validate(i) for i in result.scalars().all()]
    return items, total


async def get_dashboard_stats(db: AsyncSession) -> DashboardStats:
    today_start = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)

    jobs_today = await db.scalar(
        select(func.count()).select_from(JobPosting).where(JobPosting.crawled_at >= today_start)
    )
    jobs_total = await db.scalar(select(func.count()).select_from(JobPosting).where(JobPosting.is_active.is_(True)))
    interviews_total = await db.scalar(
        select(func.count()).select_from(InterviewPost).where(InterviewPost.status == "approved")
    )

    trend_result = await db.execute(
        select(SkillTrend, Skill)
        .join(Skill)
        .where(SkillTrend.snapshot_date >= (datetime.now(UTC).date() - timedelta(days=1)))
        .order_by(SkillTrend.count_7d.desc())
        .limit(10)
    )
    top_skills = [
        SkillTrendItem(
            skill_name=skill.name,
            count_7d=trend.count_7d,
            count_30d=trend.count_30d,
            delta_7d=trend.delta_7d,
        )
        for trend, skill in trend_result.all()
    ]

    return DashboardStats(
        jobs_today=jobs_today or 0,
        jobs_total=jobs_total or 0,
        interviews_total=interviews_total or 0,
        top_skills=top_skills,
    )
