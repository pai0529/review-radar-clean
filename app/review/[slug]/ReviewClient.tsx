"use client";

import { useEffect, useState } from "react";

type Analysis = {
  score: number;
  summary: string;
  pros: string[];
  cons: string[];
  target_users: string[];
  not_target_users: string[];
  suggestion: string;
  confidence: string;
};

type YoutubeVideo = {
  video_id: string;
  title: string;
  channel: string;
  url: string;
};

function fromSlug(slug: string) {
  return decodeURIComponent(slug).replace(/-/g, " ");
}

export default function ReviewClient({
  slug,
}: {
  slug: string;
}) {
  const productName = fromSlug(slug);

  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [youtubeVideos, setYoutubeVideos] = useState<YoutubeVideo[]>([]);
  const [youtubeCount, setYoutubeCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [statusText, setStatusText] = useState("正在搜尋多部 YouTube 評測影片...");
  const [error, setError] = useState("");

  useEffect(() => {
    async function runAnalysis() {
      setLoading(true);
      setError("");
      setStatusText("正在搜尋多部 YouTube 評測影片...");

      setTimeout(() => setStatusText("正在抓取影片留言..."), 1200);
      setTimeout(() => setStatusText("正在交給 AI 分析評論..."), 2400);

      try {
        const res = await fetch("https://review-radar-clean.onrender.com/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            product_name: productName,
            reviews: [],
            youtube_url: "",
          }),
        });

        const data = await res.json();

        if (!res.ok) {
          setError("後端發生錯誤：" + JSON.stringify(data, null, 2));
          return;
        }

        setAnalysis(data.analysis);
        setYoutubeVideos(data.youtube_videos || []);
        setYoutubeCount(data.youtube_comments_count || 0);
      } catch {
        setError("連線失敗，請確認後端 FastAPI 是否有開啟。");
      } finally {
        setLoading(false);
        setStatusText("");
      }
    }

    runAnalysis();
  }, [productName]);

  const scorePercent = analysis
    ? Math.min(100, Math.max(0, analysis.score * 10))
    : 0;

  return (
    <main className="min-h-screen bg-gradient-to-br from-zinc-950 via-zinc-900 to-black px-6 py-10 text-white">
      <section className="mx-auto max-w-6xl">
        <a href="/" className="text-sm text-zinc-400 hover:text-white">
          ← 回首頁
        </a>

        <div className="mt-8">
          <div className="mb-4 inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-zinc-300">
            AI Review Report
          </div>

          <h1 className="text-4xl font-bold md:text-6xl">
            {productName} 評價分析
          </h1>

          <p className="mt-4 max-w-2xl text-zinc-400">
            PulsePick 會自動搜尋相關 YouTube 評測影片與留言，並用 AI 整理出較客觀的口碑分析。
          </p>
        </div>

        {loading && (
          <div className="mt-8 rounded-3xl border border-white/10 bg-white/10 p-6">
            <p className="mb-4 text-zinc-300">{statusText}</p>
            <div className="mb-3 h-3 w-2/3 animate-pulse rounded bg-white/20" />
            <div className="mb-3 h-3 w-full animate-pulse rounded bg-white/20" />
            <div className="h-3 w-5/6 animate-pulse rounded bg-white/20" />
          </div>
        )}

        {error && (
          <div className="mt-8 rounded-3xl bg-red-500/20 p-6 text-red-200">
            {error}
          </div>
        )}

        {analysis && (
          <>
            <section className="mt-8 grid gap-6 lg:grid-cols-3">
              <div className="rounded-3xl bg-white p-6 text-black shadow-2xl">
                <p className="text-sm font-medium text-zinc-500">整體評分</p>

                <div className="mt-6 flex items-center justify-center">
                  <div
                    className="flex h-40 w-40 items-center justify-center rounded-full"
                    style={{
                      background: `conic-gradient(#000 ${scorePercent}%, #e5e7eb ${scorePercent}%)`,
                    }}
                  >
                    <div className="flex h-32 w-32 items-center justify-center rounded-full bg-white">
                      <div className="text-center">
                        <p className="text-4xl font-bold">{analysis.score}</p>
                        <p className="text-sm text-zinc-500">/ 10</p>
                      </div>
                    </div>
                  </div>
                </div>

                <p className="mt-6 rounded-2xl bg-zinc-100 p-4 text-sm leading-6 text-zinc-700">
                  {analysis.summary}
                </p>

                <div className="mt-4 rounded-2xl bg-black p-4 text-white">
                  <p className="text-sm text-zinc-400">可信度</p>
                  <p className="text-xl font-bold">{analysis.confidence}</p>
                </div>
              </div>

              <div className="rounded-3xl bg-white p-6 text-black shadow-2xl lg:col-span-2">
                <h2 className="mb-5 text-2xl font-bold">AI 口碑總結</h2>

                <div className="grid gap-4 md:grid-cols-2">
                  <InfoCard title="主要優點" items={analysis.pros} />
                  <InfoCard title="主要缺點" items={analysis.cons} />
                  <InfoCard title="適合哪些人" items={analysis.target_users} />
                  <InfoCard title="不適合哪些人" items={analysis.not_target_users} />
                </div>

                <div className="mt-5 rounded-2xl bg-zinc-100 p-5">
                  <p className="mb-2 text-sm font-medium text-zinc-500">
                    購買 / 使用建議
                  </p>
                  <p className="leading-7 text-zinc-800">{analysis.suggestion}</p>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-3xl bg-white p-6 text-black shadow-2xl">
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-zinc-500">
                    Data Sources
                  </p>
                  <h2 className="text-2xl font-bold">分析來源影片</h2>
                </div>

                <div className="rounded-full bg-black px-4 py-2 text-sm font-bold text-white">
                  {youtubeVideos.length} 部影片 / {youtubeCount} 則留言
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-3">
                {youtubeVideos.map((video, index) => (
                  <a
                    key={video.video_id}
                    href={video.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block rounded-2xl bg-zinc-100 p-5 transition hover:bg-zinc-200"
                  >
                    <div className="mb-3 inline-flex rounded-full bg-black px-3 py-1 text-xs font-bold text-white">
                      Source {index + 1}
                    </div>

                    <p className="line-clamp-3 font-bold">{video.title}</p>
                    <p className="mt-3 text-sm text-zinc-500">{video.channel}</p>
                    <p className="mt-4 text-sm font-medium text-zinc-700">
                      開啟 YouTube →
                    </p>
                  </a>
                ))}
              </div>
            </section>
          </>
        )}
      </section>
    </main>
  );
}

function InfoCard({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-2xl bg-zinc-100 p-5">
      <h3 className="mb-3 font-bold">{title}</h3>

      <ul className="space-y-2 text-sm text-zinc-700">
        {items && items.length > 0 ? (
          items.map((item, index) => (
            <li key={index} className="rounded-xl bg-white p-3">
              {item}
            </li>
          ))
        ) : (
          <li className="rounded-xl bg-white p-3 text-zinc-400">尚無資料</li>
        )}
      </ul>
    </div>
  );
}