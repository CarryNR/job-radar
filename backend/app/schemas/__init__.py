from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanyBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str


class JobListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    city: str | None
    salary_min: int | None
    salary_max: int | None
    experience: str | None
    source: str
    source_url: str
    crawled_at: datetime
    company: CompanyBrief
    skills: list[str] = []


class JobDetail(JobListItem):
    description: str | None
    education: str | None


class JobListResponse(BaseModel):
    items: list[JobListItem]
    total: int
    page: int
    page_size: int


class InterviewCreate(BaseModel):
    company_id: int | None = None
    company_name: str | None = Field(None, max_length=100)
    position: str = Field(..., max_length=100)
    rounds: int | None = Field(None, ge=1, le=10)
    difficulty: int | None = Field(None, ge=1, le=5)
    content: str = Field(..., min_length=20, max_length=10000)
    questions: list[str] | None = None
    author_name: str = Field(default="匿名", max_length=50)


class InterviewItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_name: str | None
    position: str
    rounds: int | None
    difficulty: int | None
    content: str
    questions: list[str] | None
    author_name: str
    likes: int
    created_at: datetime


class InterviewListResponse(BaseModel):
    items: list[InterviewItem]
    total: int
    page: int
    page_size: int


class SkillTrendItem(BaseModel):
    skill_name: str
    count_7d: int
    count_30d: int
    delta_7d: float


class DashboardStats(BaseModel):
    jobs_today: int
    jobs_total: int
    interviews_total: int
    top_skills: list[SkillTrendItem]
