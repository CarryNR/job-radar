import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Job Radar — 互联网岗位 & 面经雷达",
  description: "每日聚合大厂官网招聘岗位，技能趋势分析与面经分享",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-zinc-50 text-zinc-900 antialiased">
        <Navbar />
        <main className="max-w-5xl mx-auto px-4 py-8">{children}</main>
        <footer className="max-w-5xl mx-auto px-4 py-6 text-center text-xs text-zinc-400">
          数据来源于各公司公开招聘页，如有侵权请联系下架
        </footer>
      </body>
    </html>
  );
}
