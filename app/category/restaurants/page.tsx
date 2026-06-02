import Link from "next/link";

const restaurants = [
  {
    name: "麥當勞",
    slug: "mcdonalds",
    description:
      "全球知名速食品牌，以漢堡、薯條與快速用餐體驗聞名。"
  },

  {
    name: "肯德基",
    slug: "kfc",
    description:
      "主打炸雞與套餐的國際速食品牌。"
  },

  {
    name: "藏壽司",
    slug: "kura-sushi",
    description:
      "日本連鎖迴轉壽司品牌，以扭蛋與平價壽司受到歡迎。"
  },

  {
    name: "鼎泰豐",
    slug: "din-tai-fung",
    description:
      "台灣知名餐廳，以小籠包與精緻中式料理聞名。"
  },

  {
    name: "海底撈",
    slug: "haidilao",
    description:
      "中國連鎖火鍋品牌，以高品質服務與火鍋體驗著稱。"
  }
];

export default function RestaurantsPage() {

  return (
    <main className="min-h-screen bg-black px-6 py-16 text-white">

      <div className="mx-auto max-w-5xl">

        <a
          href="/"
          className="text-sm text-zinc-400 hover:text-white"
        >
          ← 回首頁
        </a>

        <h1 className="mt-8 text-5xl font-bold">
          Restaurants Reviews
        </h1>

        <p className="mt-4 text-zinc-400">
          PulsePick 使用 AI 整理 YouTube、
          PTT、Dcard、Reddit 等平台的餐廳真實評價。
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">

          {restaurants.map((restaurant) => (

            <Link
              key={restaurant.slug}
              href={`/review/${restaurant.slug}`}
              className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-600 hover:bg-zinc-800"
            >

              <h2 className="text-2xl font-semibold">
                {restaurant.name}
              </h2>

              <p className="mt-3 text-zinc-400">
                {restaurant.description}
              </p>

            </Link>
          ))}

        </div>
      </div>
    </main>
  );
}