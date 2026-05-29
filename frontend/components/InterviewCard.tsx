import { InterviewItem } from "@/lib/api";

export default function InterviewCard({ item }: { item: InterviewItem }) {
  return (
    <article className="p-4 rounded-lg border border-zinc-200 bg-white">
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-medium">
          {item.company_name || "未知公司"} · {item.position}
        </h3>
        {item.difficulty && (
          <span className="text-xs text-zinc-500">难度 {"★".repeat(item.difficulty)}</span>
        )}
      </div>
      <p className="text-sm text-zinc-600 line-clamp-4 whitespace-pre-wrap">{item.content}</p>
      <div className="flex items-center gap-3 mt-3 text-xs text-zinc-400">
        <span>{item.author_name}</span>
        {item.rounds && <span>{item.rounds} 轮</span>}
        <span>{new Date(item.created_at).toLocaleDateString("zh-CN")}</span>
      </div>
    </article>
  );
}
