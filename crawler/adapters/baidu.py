"""百度招聘 Adapter — 社招岗位列表。"""

import asyncio

from adapters.base import BaseSourceAdapter, JobDTO
from adapters.http_client import build_client

DEFAULT_RECRUIT_TYPE = "SOCIAL"
MAX_PAGES = 3
PAGE_SIZE = 20


class BaiduAdapter(BaseSourceAdapter):
    source_name = "baidu_careers"
    company_slug = "baidu"
    rate_limit = 1.0

    API_URL = "https://talent.baidu.com/httservice/getPostListNew"
    REFERER = "https://talent.baidu.com/jobs/social-list"

    async def fetch(self) -> list[dict]:
        jobs: list[dict] = []
        async with build_client() as client:
            for page in range(1, MAX_PAGES + 1):
                resp = await client.post(
                    self.API_URL,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                        "Referer": self.REFERER,
                    },
                    data={
                        "recruitType": DEFAULT_RECRUIT_TYPE,
                        "curPage": str(page),
                        "pageSize": str(PAGE_SIZE),
                        "keyWord": "",
                        "projectType": "",
                        "workPlace": "",
                        "postType": "",
                    },
                )
                resp.raise_for_status()
                payload = resp.json()
                if payload.get("status") != "ok":
                    raise RuntimeError(payload.get("message", "百度招聘 API 返回失败"))

                batch = payload.get("data", {}).get("list", [])
                if not batch:
                    break
                jobs.extend(batch)
                if len(batch) < PAGE_SIZE:
                    break
                if page < MAX_PAGES:
                    await asyncio.sleep(1 / self.rate_limit)
        return jobs

    def parse(self, raw: dict) -> JobDTO | None:
        title = raw.get("name")
        post_id = raw.get("postId")
        if not title or not post_id:
            return None

        work_place = raw.get("workPlace", "")
        city = work_place.split(",")[0] if work_place else None
        work_content = raw.get("workContent") or ""
        service_condition = raw.get("serviceCondition") or ""
        description = (work_content or service_condition or title)[:500]

        return JobDTO(
            company_slug=self.company_slug,
            title=title.strip(),
            city=city,
            salary_min=None,
            salary_max=None,
            experience=raw.get("workYears") or None,
            education=raw.get("education") or None,
            description=description,
            source_url=f"https://talent.baidu.com/jobs/detail/{DEFAULT_RECRUIT_TYPE}/{post_id}",
            source=self.source_name,
        )


if __name__ == "__main__":
    adapter = BaiduAdapter()

    async def main():
        jobs = await adapter.run()
        print(f"Fetched {len(jobs)} jobs")
        for job in jobs[:3]:
            print(f"  - {job.title} ({job.city})")

    asyncio.run(main())
