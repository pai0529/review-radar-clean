import Link from "next/link";

const tools = [
  { name: "TikTok", slug: "tiktok", domain: "tiktok.com", description: "全球熱門短影音平台，以高黏著度推薦演算法聞名。" },
  { name: "Instagram", slug: "instagram", domain: "instagram.com", description: "Meta 旗下社群平台，主打照片、Reels 與社交互動。" },
  { name: "Discord", slug: "discord", domain: "discord.com", description: "熱門語音與社群聊天平台，深受遊戲與創作者社群喜愛。" },
  { name: "Spotify", slug: "spotify", domain: "spotify.com", description: "全球知名音樂串流平台，提供個人化推薦與 Podcast。" },
  { name: "Netflix", slug: "netflix", domain: "netflix.com", description: "全球影音串流平台，擁有大量原創影集與電影內容。" },
];

function faviconUrl(domain: string) {
  return `https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://${domain}&size=256`;
}

export default function AppsPage() {
  return (
    <main className="min-h-screen bg-black px-6 py-16 text-white">
      <div className="mx-auto max-w-5xl">

        <a href="/" className="text-sm text-zinc-400 hover:text-white">← 回首頁</a>

        <h1 className="mt-8 text-5xl font-bold">Apps Reviews</h1>
        <p className="mt-4 text-zinc-400">
          PulsePick 使用 AI 整理 YouTube、PTT、Dcard、Reddit 等平台的真實評價。
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {tools.map((tool) => (
            <Link
              key={tool.slug}
              href={`/review/${tool.slug}`}
              className="flex items-center gap-5 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-600 hover:bg-zinc-800"
            >
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-white p-2">
                <img
                  src={faviconUrl(tool.domain)}
                  alt={tool.name}
                  className="h-12 w-12 object-contain"
                />
              </div>
              <div>
                <h2 className="text-xl font-semibold">{tool.name}</h2>
                <p className="mt-1 text-sm text-zinc-400">{tool.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
