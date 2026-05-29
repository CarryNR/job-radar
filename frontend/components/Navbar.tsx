import Link from "next/link";

const NAV = [
  { href: "/", label: "首页" },
  { href: "/jobs", label: "岗位" },
  { href: "/interviews", label: "面经" },
  { href: "/trends", label: "趋势" },
  { href: "/interviews/new", label: "投稿" },
];

export default function Navbar() {
  return (
    <header className="border-b border-zinc-200 bg-white/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="font-semibold text-lg tracking-tight">
          Job Radar
        </Link>
        <nav className="flex gap-1 sm:gap-4 text-sm">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="px-2 py-1 rounded-md text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100 transition-colors"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
