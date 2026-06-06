"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

function toSlug(text: string) {
  return text
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\w\u4e00-\u9fa5-]/g, "");
}

export default function Home() {
  const [query, setQuery] = useState("");
  const router = useRouter();

  function handleSearch() {
    if (!query.trim()) return;
    router.push(`/review/${toSlug(query)}`);
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-zinc-950 via-zinc-900 to-black px-6 text-white">
      <section className="w-full max-w-4xl text-center">

        {/* Badge */}
        <div className="mb-4 inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-zinc-300">
          AI 商品口碑搜尋引擎
        </div>

        {/* Title */}
        <h1 className="text-5xl font-bold md:text-7xl">
          PulsePick
        </h1>

        {/* Description */}
        <p className="mx-auto mt-5 max-w-2xl text-zinc-400">
          搜尋你想了解的商品或 App，
          AI 會整理多個平台的評論，
          產生客觀評分、優缺點與購買建議。
        </p>

        {/* Search Box */}
        <div className="mt-8 flex flex-col gap-3 rounded-3xl border border-white/10 bg-white/10 p-4 backdrop-blur md:flex-row">

          <input
            className="flex-1 rounded-2xl bg-black/40 p-4 text-white outline-none placeholder:text-zinc-500"
            placeholder="例如：Nike Air Force 1、ChatGPT Plus、iPhone"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSearch();
            }}
          />

          <button
            onClick={handleSearch}
            className="rounded-2xl bg-white px-8 py-4 font-bold text-black transition hover:bg-zinc-200"
          >
            搜尋評價
          </button>
        </div>

        {/* Hot Searches */}
        <div className="mt-10">
          <p className="mb-4 text-sm text-zinc-500">熱門搜尋</p>
          <div className="flex flex-wrap justify-center gap-2">
            {["iPhone 15", "ChatGPT", "Galaxy S24", "Netflix", "PS5", "鼎泰豐", "Cursor", "Nintendo Switch 2"].map((item) => (
              <button
                key={item}
                onClick={() => {
                  setQuery(item);
                  router.push(`/review/${item.trim().toLowerCase().replace(/\s+/g, "-").replace(/[^\w一-龥-]/g, "")}`);
                }}
                className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-zinc-300 transition hover:bg-white hover:text-black"
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* Categories */}
        <div className="mt-8">
          <p className="mb-4 text-sm text-zinc-500">熱門分類</p>
          <div className="flex flex-wrap justify-center gap-3">
            <a href="/category/ai-tools" className="rounded-full border border-white/10 bg-white/5 px-5 py-3 text-sm text-zinc-300 transition hover:bg-white hover:text-black">AI Tools</a>
            <a href="/category/3c" className="rounded-full border border-white/10 bg-white/5 px-5 py-3 text-sm text-zinc-300 transition hover:bg-white hover:text-black">3C</a>
            <a href="/category/apps" className="rounded-full border border-white/10 bg-white/5 px-5 py-3 text-sm text-zinc-300 transition hover:bg-white hover:text-black">Apps</a>
            <a href="/category/restaurants" className="rounded-full border border-white/10 bg-white/5 px-5 py-3 text-sm text-zinc-300 transition hover:bg-white hover:text-black">Restaurants</a>
          </div>
        </div>

      </section>
    </main>
  );
}