import JobCard from "@/components/JobCard";
import { getJobs } from "@/lib/api";

export default async function JobsPage({
  searchParams,
}: {
  searchParams: { page?: string; city?: string; keyword?: string };
}) {
  const page = Number(searchParams.page) || 1;
  let data = { items: [] as Awaited<ReturnType<typeof getJobs>>["items"], total: 0, page: 1, page_size: 20 };

  try {
    data = await getJobs({ page, city: searchParams.city, keyword: searchParams.keyword });
  } catch {
    /* empty */
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">岗位列表</h1>

      <form className="flex gap-2">
        <input
          name="keyword"
          defaultValue={searchParams.keyword}
          placeholder="搜索岗位关键词..."
          className="flex-1 px-3 py-2 rounded-lg border border-zinc-200 text-sm"
        />
        <button type="submit" className="px-4 py-2 rounded-lg bg-zinc-900 text-white text-sm">
          搜索
        </button>
      </form>

      {data.items.length === 0 ? (
        <p className="text-zinc-400 text-sm">暂无岗位数据</p>
      ) : (
        <div className="space-y-3">
          {data.items.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      )}

      <p className="text-sm text-zinc-400">
        共 {data.total} 条 · 第 {data.page} 页
      </p>
    </div>
  );
}
