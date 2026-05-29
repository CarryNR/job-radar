const API_URL =
  typeof window === "undefined"
    ? process.env.INTERNAL_API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
    : process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface CompanyBrief {
  id: number;
  name: string;
  slug: string;
}

export interface JobListItem {
  id: number;
  title: string;
  city: string | null;
  salary_min: number | null;
  salary_max: number | null;
  experience: string | null;
  source: string;
  source_url: string;
  crawled_at: string;
  company: CompanyBrief;
  skills: string[];
}

export interface JobListResponse {
  items: JobListItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface DashboardStats {
  jobs_today: number;
  jobs_total: number;
  interviews_total: number;
  top_skills: { skill_name: string; count_7d: number; count_30d: number; delta_7d: number }[];
}

export interface InterviewItem {
  id: number;
  company_name: string | null;
  position: string;
  rounds: number | null;
  difficulty: number | null;
  content: string;
  questions: string[] | null;
  author_name: string;
  likes: number;
  created_at: string;
}

export interface InterviewListResponse {
  items: InterviewItem[];
  total: number;
  page: number;
  page_size: number;
}

async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}/api${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
    next: { revalidate: 60 },
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function getStats() {
  return fetchApi<DashboardStats>("/stats");
}

export function getJobs(params?: { page?: number; city?: string; keyword?: string }) {
  const qs = new URLSearchParams();
  if (params?.page) qs.set("page", String(params.page));
  if (params?.city) qs.set("city", params.city);
  if (params?.keyword) qs.set("keyword", params.keyword);
  const query = qs.toString();
  return fetchApi<JobListResponse>(`/jobs${query ? `?${query}` : ""}`);
}

export function getJob(id: number) {
  return fetchApi<JobListItem & { description?: string; education?: string }>(`/jobs/${id}`);
}

export function getInterviews(page = 1) {
  return fetchApi<InterviewListResponse>(`/interviews?page=${page}`);
}

export function createInterview(data: {
  company_name?: string;
  position: string;
  rounds?: number;
  difficulty?: number;
  content: string;
  author_name?: string;
}) {
  return fetch(`${API_URL}/api/interviews`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export function formatSalary(min: number | null, max: number | null): string {
  if (!min && !max) return "面议";
  if (min && max && min !== max) return `${min / 1000}k-${max / 1000}k`;
  const val = (min || max)!;
  return `${val / 1000}k`;
}
