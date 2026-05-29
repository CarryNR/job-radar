import Link from "next/link";
import { formatSalary, getJob } from "@/lib/api";

export default async function JobDetailPage({ params }: { params: { id: string } }) {
  let job: Awaited<ReturnType<typeof getJob>> | null = null;
  try {
    job = await getJob(Number(params.id));
  } catch {
    /* not found */
  }

  if (!job) {
    return (
      <div className="text-center py-12">
        <p className="text-zinc-400">岗位不存在</p>
        <Link href="/jobs" className="text-emerald-600 text-sm mt-2 inline-block">
          返回列表
        </Link>
      </div>
    );
  }

  return (
    <article className="space-y-6">
      <div>
        <Link href="/jobs" className="text-sm text-zinc-400 hover:text-zinc-600">
          ← 返回列表
        </Link>
        <h1 className="text-2xl font-bold mt-2">{job.title}</h1>
        <p className="text-zinc-500 mt-1">
          {job.company.name}
          {job.city && ` · ${job.city}`}
          {job.experience && ` · ${job.experience}`}
          {" · "}
          {formatSalary(job.salary_min, job.salary_max)}
        </p>
      </div>

      {job.skills.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {job.skills.map((s) => (
            <span key={s} className="px-2 py-1 rounded-full bg-zinc-100 text-sm">
              {s}
            </span>
          ))}
        </div>
      )}

      {job.description && (
        <section>
          <h2 className="font-semibold mb-2">岗位摘要</h2>
          <p className="text-sm text-zinc-600 whitespace-pre-wrap leading-relaxed">{job.description}</p>
        </section>
      )}

      <a
        href={job.source_url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm hover:bg-emerald-700"
      >
        查看原站详情 →
      </a>
    </article>
  );
}
