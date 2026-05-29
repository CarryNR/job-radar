import { getStats } from "@/lib/api";

export default async function TrendsPage() {
  let stats = { top_skills: [] as { skill_name: string; count_7d: number; count_30d: number; delta_7d: number }[] };

  try {
    stats = await getStats();
  } catch {
    /* empty */
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">技能趋势</h1>
      <p className="text-sm text-zinc-500">基于近 7 天岗位 JD 中出现的技能标签统计</p>

      {stats.top_skills.length === 0 ? (
        <p className="text-zinc-400 text-sm">暂无趋势数据，请先运行爬虫积累数据</p>
      ) : (
        <div className="space-y-3">
          {stats.top_skills.map((s, i) => (
            <div key={s.skill_name} className="flex items-center gap-4 p-3 rounded-lg bg-white border border-zinc-200">
              <span className="text-zinc-400 w-6 text-right text-sm">{i + 1}</span>
              <span className="font-medium flex-1">{s.skill_name}</span>
              <div className="flex-1 h-2 bg-zinc-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-500 rounded-full"
                  style={{ width: `${Math.min(100, (s.count_7d / (stats.top_skills[0]?.count_7d || 1)) * 100)}%` }}
                />
              </div>
              <span className="text-sm text-zinc-500 w-16 text-right">{s.count_7d} 次</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
