import os
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from app.models import Company, CrawlLog, JobPosting, JobSkill, Skill  # noqa: E402
from adapters.base import JobDTO  # noqa: E402
from pipeline.normalize import normalize_city, truncate_description  # noqa: E402
from pipeline.skill_extract import extract_skills  # noqa: E402


async def upsert_jobs(session: AsyncSession, jobs: list[JobDTO], source: str) -> tuple[int, int]:
    new_count = 0
    updated_count = 0

    for dto in jobs:
        company_result = await session.execute(select(Company).where(Company.slug == dto.company_slug))
        company = company_result.scalar_one_or_none()
        if not company:
            continue

        dto.city = normalize_city(dto.city)
        dto.description = truncate_description(dto.description)
        skills = dto.skills or extract_skills(f"{dto.title} {dto.description}")

        existing = await session.execute(select(JobPosting).where(JobPosting.fingerprint == dto.fingerprint))
        job = existing.scalar_one_or_none()

        if job:
            job.title = dto.title
            job.city = dto.city
            job.description = dto.description
            job.source_url = dto.source_url
            job.is_active = True
            job.updated_at = datetime.now(timezone.utc)
            updated_count += 1
        else:
            job = JobPosting(
                company_id=company.id,
                title=dto.title,
                city=dto.city,
                salary_min=dto.salary_min,
                salary_max=dto.salary_max,
                experience=dto.experience,
                education=dto.education,
                description=dto.description,
                source=dto.source,
                source_url=dto.source_url,
                fingerprint=dto.fingerprint,
                is_active=True,
            )
            session.add(job)
            await session.flush()
            new_count += 1

        for skill_name in skills:
            skill_result = await session.execute(select(Skill).where(Skill.name == skill_name))
            skill = skill_result.scalar_one_or_none()
            if not skill:
                skill = Skill(name=skill_name)
                session.add(skill)
                await session.flush()

            link = await session.execute(
                select(JobSkill).where(JobSkill.job_id == job.id, JobSkill.skill_id == skill.id)
            )
            if not link.scalar_one_or_none():
                session.add(JobSkill(job_id=job.id, skill_id=skill.id))

    log = CrawlLog(
        source=source,
        status="success",
        jobs_new=new_count,
        jobs_updated=updated_count,
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
    )
    session.add(log)
    await session.commit()
    return new_count, updated_count


async def run_adapter(adapter_class, database_url: str) -> None:
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    adapter = adapter_class()
    started = datetime.now(timezone.utc)

    try:
        jobs = await adapter.run()
        async with session_factory() as session:
            new_count, updated_count = await upsert_jobs(session, jobs, adapter.source_name)
        print(f"[{adapter.source_name}] new={new_count}, updated={updated_count}")
    except Exception as e:
        async with session_factory() as session:
            session.add(
                CrawlLog(
                    source=adapter.source_name,
                    status="failed",
                    error_msg=str(e),
                    started_at=started,
                    finished_at=datetime.now(timezone.utc),
                )
            )
            await session.commit()
        print(f"[{adapter.source_name}] FAILED: {e}")
        raise
    finally:
        await engine.dispose()
