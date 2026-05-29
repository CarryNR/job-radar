import Link from "next/link";
import { JobListItem, formatSalary } from "@/lib/api";

export default function JobCard({ job }: { job: JobListItem }) {
  return (
    <Link
      href={`/jobs/${job.id}`}
      className="block p-4 rounded-lg border border-zinc-200 hover:border-zinc-400 hover:shadow-sm transition-all bg-white"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-medium text-zinc-900">{job.title}</h3>
          <p className="text-sm text-zinc-500 mt-1">
            {job.company.name}
            {job.city && ` · ${job.city}`}
            {job.experience && ` · ${job.experience}`}
          </p>
        </div>
        <span className="text-sm font-medium text-emerald-600 whitespace-nowrap">
          {formatSalary(job.salary_min, job.salary_max)}
        </span>
      </div>
      {job.skills.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3">
          {job.skills.map((s) => (
            <span key={s} className="text-xs px-2 py-0.5 rounded-full bg-zinc-100 text-zinc-600">
              {s}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
