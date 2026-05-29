"""京东招聘 Adapter — 官方校招/实习岗位。

说明：zhaopin.jd.com 社招接口需登录，此处使用 campus.jd.com 公开 API。
"""

import asyncio

from adapters.base import BaseSourceAdapter, JobDTO
from adapters.http_client import build_client

PAGE_SIZE = 10


class JDAdapter(BaseSourceAdapter):
    source_name = "jd_campus"
    company_slug = "jd"
    rate_limit = 1.0

    API_URL = "https://campus.jd.com/api/wx/position/page?type=present"

    async def fetch(self) -> list[dict]:
        jobs: list[dict] = []
        page_index = 1

        async with build_client() as client:
            while True:
                resp = await client.post(
                    self.API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Referer": "https://campus.jd.com/",
                        "Origin": "https://campus.jd.com",
                    },
                    json={
                        "pageSize": PAGE_SIZE,
                        "pageIndex": page_index,
                        "parameter": {
                            "positionName": "",
                            "planIdList": [],
                        },
                    },
                )
                resp.raise_for_status()
                payload = resp.json()
                if not payload.get("success"):
                    raise RuntimeError("京东招聘 API 返回失败")

                body = payload.get("body", {})
                batch = body.get("items", [])
                if not batch:
                    break

                jobs.extend(batch)
                total = body.get("totalNumber", 0)
                if len(jobs) >= total:
                    break

                page_index += 1
                await asyncio.sleep(1 / self.rate_limit)

        return jobs

    def parse(self, raw: dict) -> JobDTO | None:
        title = raw.get("positionName")
        publish_id = raw.get("publishId")
        if not title or not publish_id:
            return None

        requirements = raw.get("requirementVoList") or []
        city = None
        if requirements:
            work_city = requirements[0].get("workCity") or ""
            city = work_city.split("-")[-1] if work_city else None

        work_content = raw.get("workContent") or ""
        qualification = raw.get("qualification") or ""
        description = (work_content or qualification or title)[:500]

        return JobDTO(
            company_slug=self.company_slug,
            title=title.strip(),
            city=city,
            salary_min=None,
            salary_max=None,
            experience=None,
            education=None,
            description=description,
            source_url=f"https://campus.jd.com/#/newDetails?publishId={publish_id}",
            source=self.source_name,
        )


if __name__ == "__main__":
    adapter = JDAdapter()

    async def main():
        jobs = await adapter.run()
        print(f"Fetched {len(jobs)} jobs")
        for job in jobs[:3]:
            print(f"  - {job.title} ({job.city})")

    asyncio.run(main())
