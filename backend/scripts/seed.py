"""Seed companies and skills."""

import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models import Company, Skill

COMPANIES = [
    ("字节跳动", "bytedance", "https://jobs.bytedance.com"),
    ("阿里巴巴", "alibaba", "https://talent.alibaba.com"),
    ("腾讯", "tencent", "https://careers.tencent.com"),
    ("美团", "meituan", "https://zhaopin.meituan.com"),
    ("京东", "jd", "https://zhaopin.jd.com"),
    ("百度", "baidu", "https://talent.baidu.com"),
    ("网易", "netease", "https://game.campus.163.com"),
    ("小米", "xiaomi", "https://hr.xiaomi.com"),
    ("拼多多", "pinduoduo", "https://careers.pinduoduo.com"),
    ("快手", "kuaishou", "https://zhaopin.kuaishou.cn"),
]

SKILLS = [
    ("Java", "language"),
    ("Python", "language"),
    ("Go", "language"),
    ("Rust", "language"),
    ("C++", "language"),
    ("JavaScript", "language"),
    ("TypeScript", "language"),
    ("React", "framework"),
    ("Vue", "framework"),
    ("Node.js", "framework"),
    ("Spring", "framework"),
    ("MySQL", "tool"),
    ("Redis", "tool"),
    ("Kafka", "tool"),
    ("Kubernetes", "tool"),
    ("Docker", "tool"),
    ("PyTorch", "tool"),
    ("TensorFlow", "tool"),
    ("机器学习", "domain"),
    ("深度学习", "domain"),
]


async def seed_companies(database_url: str):
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        for name, slug, url in COMPANIES:
            exists = await session.execute(select(Company).where(Company.slug == slug))
            if exists.scalar_one_or_none():
                continue
            session.add(Company(name=name, slug=slug, careers_url=url, industry="internet"))
        await session.commit()
    await engine.dispose()
    print(f"Seeded {len(COMPANIES)} companies")


async def seed_skills(database_url: str):
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        for name, category in SKILLS:
            exists = await session.execute(select(Skill).where(Skill.name == name))
            if exists.scalar_one_or_none():
                continue
            session.add(Skill(name=name, category=category))
        await session.commit()
    await engine.dispose()
    print(f"Seeded {len(SKILLS)} skills")


async def main():
    url = os.getenv("DATABASE_URL", "postgresql+asyncpg://jobradar:jobradar_dev@localhost:5432/jobradar")
    await seed_companies(url)
    await seed_skills(url)


if __name__ == "__main__":
    asyncio.run(main())
