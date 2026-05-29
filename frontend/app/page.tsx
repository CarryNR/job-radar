import Link from "next/link";
import JobCard from "@/components/JobCard";
import { getJobs, getStats } from "@/lib/api";

export default async function Home() {
  let stats = { jobs_today: 0, jobs_total: 0, interviews_total: 0, top_skills: [] as { skill_name: string; count_7d: number }[] };
  let jobs: Awaited<ReturnType<typeof getJobs>>["items"] = [];

  try {
    [stats, { items: jobs }] = await Promise.all([getStats(), getJobs({ page: 1 })]);
  } catch {
    /* API 未启动时展示空状态 */
  }

  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-2xl font-bold tracking-tight">互联网岗位 & 面经雷达</h1>
        <p className="text-zinc-500 mt-2">低调看行情，每日更新大厂官网招聘岗位</p>
      </section>

      <section className="grid grid-cols-3 gap-4">
        {[
          { label: "今日新增", value: stats.jobs_today },
          { label: "在招岗位", value: stats.jobs_total },
          { label: "面经收录", value: stats.interviews_total },
        ].map((s) => (
          <div key={s.label} className="p-4 rounded-lg bg-white border border-zinc-200 text-center">
            <div className="text-2xl font-bold">{s.value}</div>
            <div className="text-sm text-zinc-500 mt-1">{s.label}</div>
          </div>
        ))}
      </section>

      {stats.top_skills.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold mb-3">热门技能</h2>
          <div className="flex flex-wrap gap-2">
            {stats.top_skills.map((s) => (
              <span key={s.skill_name} className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-sm">
                {s.skill_name} ({s.count_7d})
              </span>
            ))}
          </div>
        </section>
      )}

      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">最新岗位</h2>
          <Link href="/jobs" className="text-sm text-emerald-600 hover:underline">
            查看全部 →
          </Link>
        </div>
        {jobs.length === 0 ? (
          <p className="text-zinc-400 text-sm">暂无数据，请先启动后端并运行爬虫</p>
        ) : (
          <div className="space-y-3">
            {jobs.slice(0, 5).map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
