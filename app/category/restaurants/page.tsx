import Link from "next/link";

const restaurants = [
  { name: "麥當勞", slug: "mcdonalds", domain: "mcdonalds.com", description: "全球知名速食品牌，以漢堡、薯條與快速用餐體驗聞名。" },
  { name: "肯德基", slug: "kfc", domain: "kfc.com", description: "主打炸雞與套餐的國際速食品牌。" },
  { name: "藏壽司", slug: "kura-sushi", domain: "kurasushi.com", description: "日本連鎖迴轉壽司品牌，以扭蛋與平價壽司受到歡迎。" },
  { name: "鼎泰豐", slug: "din-tai-fung", domain: "dintaifung.com.tw", description: "台灣知名餐廳，以小籠包與精緻中式料理聞名。" },
  { name: "海底撈", slug: "haidilao", domain: "haidilao.com", description: "中國連鎖火鍋品牌，以高品質服務與火鍋體驗著稱。" },
];

function faviconUrl(domain: string) {
  return `https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://${domain}&size=256`;
}

export default function RestaurantsPage() {
  return (
    <main className="min-h-screen bg-black px-6 py-16 text-white">
      <div className="mx-auto max-w-5xl">

        <a href="/" className="text-sm text-zinc-400 hover:text-white">← 回首頁</a>

        <h1 className="mt-8 text-5xl font-bold">Restaurants Reviews</h1>
        <p className="mt-4 text-zinc-400">
          PulsePick 使用 AI 整理 YouTube、PTT、Dcard、Reddit 等平台的餐廳真實評價。
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {restaurants.map((r) => (
            <Link
              key={r.slug}
              href={`/review/${r.slug}`}
              className="flex items-center gap-5 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-600 hover:bg-zinc-800"
            >
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-white p-2">
                <img
                  src={faviconUrl(r.domain)}
                  alt={r.name}
                  className="h-12 w-12 object-contain"
                />
              </div>
              <div>
                <h2 className="text-xl font-semibold">{r.name}</h2>
                <p className="mt-1 text-sm text-zinc-400">{r.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
