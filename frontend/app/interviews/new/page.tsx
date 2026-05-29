"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { createInterview } from "@/lib/api";

export default function NewInterviewPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const form = new FormData(e.currentTarget);
    const res = await createInterview({
      company_name: form.get("company_name") as string,
      position: form.get("position") as string,
      rounds: Number(form.get("rounds")) || undefined,
      difficulty: Number(form.get("difficulty")) || undefined,
      content: form.get("content") as string,
      author_name: (form.get("author_name") as string) || "匿名",
    });

    setLoading(false);
    if (res.ok) {
      router.push("/interviews");
    } else {
      setError("提交失败，请检查内容后重试");
    }
  }

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">分享面经</h1>
      <p className="text-sm text-zinc-500">投稿后需审核通过才会公开显示，请勿包含个人联系方式</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="company_name" placeholder="公司名称 *" required className="w-full px-3 py-2 rounded-lg border border-zinc-200 text-sm" />
        <input name="position" placeholder="岗位方向 *（如：后端开发）" required className="w-full px-3 py-2 rounded-lg border border-zinc-200 text-sm" />
        <div className="flex gap-4">
          <input name="rounds" type="number" min={1} max={10} placeholder="面试轮次" className="flex-1 px-3 py-2 rounded-lg border border-zinc-200 text-sm" />
          <select name="difficulty" className="flex-1 px-3 py-2 rounded-lg border border-zinc-200 text-sm">
            <option value="">难度</option>
            {[1, 2, 3, 4, 5].map((d) => (
              <option key={d} value={d}>{"★".repeat(d)}</option>
            ))}
          </select>
        </div>
        <textarea name="content" placeholder="面经内容 *（题目、流程、感受...）" required rows={8} className="w-full px-3 py-2 rounded-lg border border-zinc-200 text-sm" />
        <input name="author_name" placeholder="昵称（默认匿名）" className="w-full px-3 py-2 rounded-lg border border-zinc-200 text-sm" />

        {error && <p className="text-sm text-red-500">{error}</p>}

        <button type="submit" disabled={loading} className="w-full py-2 rounded-lg bg-zinc-900 text-white text-sm disabled:opacity-50">
          {loading ? "提交中..." : "提交面经"}
        </button>
      </form>
    </div>
  );
}
