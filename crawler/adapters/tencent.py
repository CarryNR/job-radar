"""腾讯招聘 Adapter 模板。

实际页面结构可能变化，需根据 careers.tencent.com 当前 DOM/API 调整 fetch/parse。
"""

import asyncio
import time

import httpx

from adapters.base import BaseSourceAdapter, JobDTO


class TencentAdapter(BaseSourceAdapter):
    source_name = "tencent_careers"
    company_slug = "tencent"
    rate_limit = 1.0

    API_URL = "https://careers.tencent.com/tencentcareer/api/post/Query"

    async def fetch(self) -> list[dict]:
        params = {
            "timestamp": str(int(time.time() * 1000)),
            "countryId": "1",
            "pageIndex": "1",
            "pageSize": "50",
            "language": "zh-cn",
            "area": "cn",
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(self.API_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            return data.get("Data", {}).get("Posts", [])

    def parse(self, raw: dict) -> JobDTO | None:
        title = raw.get("RecruitPostName")
        if not title:
            return None

        location = raw.get("LocationName", "")
        desc = raw.get("Responsibility", "") or raw.get("RequireWorkYearsName", "")
        post_id = raw.get("PostId", "")
        source_url = f"https://careers.tencent.com/jobdesc.html?postId={post_id}"

        return JobDTO(
            company_slug=self.company_slug,
            title=title.strip(),
            city=location.split(",")[0] if location else None,
            salary_min=None,
            salary_max=None,
            experience=raw.get("RequireWorkYearsName"),
            education=raw.get("RequireEducationName"),
            description=(desc or title)[:500],
            source_url=source_url,
            source=self.source_name,
        )


if __name__ == "__main__":
    adapter = TencentAdapter()

    async def main():
        jobs = await adapter.run()
        print(f"Fetched {len(jobs)} jobs")
        for job in jobs[:3]:
            print(f"  - {job.title} ({job.city})")

    asyncio.run(main())
