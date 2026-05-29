from abc import ABC, abstractmethod
from dataclasses import dataclass
import hashlib


@dataclass
class JobDTO:
    company_slug: str
    title: str
    city: str | None
    salary_min: int | None
    salary_max: int | None
    experience: str | None
    education: str | None
    description: str
    source_url: str
    source: str
    skills: list[str] | None = None

    @property
    def fingerprint(self) -> str:
        raw = f"{self.company_slug}|{self.title}|{self.city}|{self.salary_min}|{self.salary_max}"
        return hashlib.sha256(raw.encode()).hexdigest()


class BaseSourceAdapter(ABC):
    source_name: str
    company_slug: str
    rate_limit: float = 1.0

    @abstractmethod
    async def fetch(self) -> list[dict]:
        """拉取原始数据列表"""

    @abstractmethod
    def parse(self, raw: dict) -> JobDTO | None:
        """解析单条记录"""

    async def run(self) -> list[JobDTO]:
        raw_list = await self.fetch()
        jobs: list[JobDTO] = []
        for raw in raw_list:
            job = self.parse(raw)
            if job:
                jobs.append(job)
        return jobs
