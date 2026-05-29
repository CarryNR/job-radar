import InterviewCard from "@/components/InterviewCard";
import Link from "next/link";
import { getInterviews } from "@/lib/api";

export default async function InterviewsPage() {
  let data = { items: [] as Awaited<ReturnType<typeof getInterviews>>["items"], total: 0 };

  try {
    data = await getInterviews();
  } catch {
    /* empty */
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">面经库</h1>
        <Link href="/interviews/new" className="px-4 py-2 rounded-lg bg-zinc-900 text-white text-sm">
          分享面经
        </Link>
      </div>

      {data.items.length === 0 ? (
        <p className="text-zinc-400 text-sm">暂无面经，成为第一个分享者吧</p>
      ) : (
        <div className="space-y-4">
          {data.items.map((item) => (
            <InterviewCard key={item.id} item={item} />
          ))}
        </div>
      )}

      <p className="text-sm text-zinc-400">共 {data.total} 条面经</p>
    </div>
  );
}
