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

function fromSlug(slug: string) {
  return decodeURIComponent(slug).replace(/-/g, " ");
}

export default function ReviewClient({ slug }: { slug: string }) {
  const productName = fromSlug(slug);

  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [imageUrl, setImageUrl] = useState("");
  const [imageType, setImageType] = useState("logo");
  const [youtubeCount, setYoutubeCount] = useState(0);
  const [tavilyCount, setTavilyCount] = useState(0);
  const [cached, setCached] = useState(false);
  const [loading, setLoading] = useState(true);
  const [statusText, setStatusText] = useState("正在搜尋多平台評價...");
  const [error, setError] = useState("");

  useEffect(() => {
    async function runAnalysis() {
      setLoading(true);
      setError("");
      setStatusText("正在搜尋多平台評價...");

      setTimeout(() => setStatusText("正在整理 YouTube 與網路討論..."), 1200);
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
        setImageUrl(data.image_url || "");
        setImageType(data.image_type || "logo");
        setYoutubeCount(data.youtube_comments_count || 0);
        setTavilyCount(data.tavily_results_count || 0);
        setCached(data.cached || false);
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

  const imageClass =
    imageType === "product"
      ? "max-h-44 max-w-full object-contain"
      : imageType === "app_logo"
      ? "h-28 w-28 object-contain rounded-2xl"
      : "max-h-28 max-w-28 object-contain";

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
            PulsePick 會整合 YouTube 與網路搜尋結果，
            並利用 AI 產生客觀的口碑分析與購買建議。
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
            <section className="mt-8 grid gap-6 rounded-3xl border border-white/10 bg-white/10 p-6 backdrop-blur md:grid-cols-[220px_1fr]">
              <div className="flex h-56 items-center justify-center rounded-3xl bg-white p-6">
                {imageUrl ? (
                  <img
                    src={imageUrl}
                    alt={productName}
                    className={imageClass}
                  />
                ) : (
                  <div className="flex h-32 w-32 items-center justify-center rounded-3xl bg-black text-5xl font-bold text-white">
                    {productName.slice(0, 1).toUpperCase()}
                  </div>
                )}
              </div>

              <div className="flex flex-col justify-center text-left">
                <p className="text-sm text-zinc-400">
                  PulsePick AI Review
                </p>

                <h2 className="mt-2 text-3xl font-bold md:text-5xl">
                  {productName}
                </h2>

                <p className="mt-4 max-w-2xl leading-7 text-zinc-400">
                  AI 會整理 YouTube 與多平台搜尋結果，分析這個項目的整體口碑、優缺點與使用建議。
                </p>

                <div className="mt-5 flex flex-wrap gap-3">
                  <span className="rounded-full bg-white px-4 py-2 text-sm font-bold text-black">
                    {cached ? "已快取結果" : "即時分析"}
                  </span>

                  <span className="rounded-full border border-white/10 px-4 py-2 text-sm text-zinc-300">
                    {tavilyCount} 筆網路結果
                  </span>

                  <span className="rounded-full border border-white/10 px-4 py-2 text-sm text-zinc-300">
                    {youtubeCount} 則 YouTube 留言
                  </span>
                </div>
              </div>
            </section>

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
              <div className="mb-5">
                <p className="text-sm font-medium text-zinc-500">
                  Data Sources
                </p>
                <h2 className="text-2xl font-bold">本次分析資料來源</h2>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <SourceCard title="YouTube 留言" count={youtubeCount} />
                <SourceCard title="網路搜尋結果" count={tavilyCount} />
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
          <li className="rounded-xl bg-white p-3 text-zinc-400">
            尚無資料
          </li>
        )}
      </ul>
    </div>
  );
}

function SourceCard({ title, count }: { title: string; count: number }) {
  return (
    <div className="rounded-2xl bg-zinc-100 p-5">
      <p className="text-sm text-zinc-500">{title}</p>
      <p className="mt-2 text-3xl font-bold">{count}</p>
      <p className="mt-1 text-xs text-zinc-400">筆資料</p>
    </div>
  );
}