import Link from "next/link";

const tools = [
  {
    name: "iPhone 15",
    slug: "iphone-15",
    description:
      "Apple 智慧型手機，主打動態島、USB-C 與穩定的 iOS 體驗。"
  },

  {
    name: "Galaxy S24",
    slug: "galaxy-s24",
    description:
      "Samsung 旗艦 Android 手機，強調 AI 功能與高階相機體驗。"
  },

  {
    name: "ROG Phone",
    slug: "rog-phone",
    description:
      "專為遊戲玩家打造的高效能 Android 電競手機。"
  },

  {
    name: "Google Pixel 9",
    slug: "google-pixel-9",
    description:
      "Google 推出的 AI 智慧型手機，擅長拍照與原生 Android 體驗。"
  },

  {
    name: "Xiaomi 14",
    slug: "xiaomi-14",
    description:
      "高 CP 值旗艦手機，兼具性能、續航與 Leica 相機系統。"
  },

  {
    name: "Steam Deck",
    slug: "steam-deck",
    description:
      "Valve 推出的掌上型 PC 遊戲主機，可遊玩大量 Steam 遊戲。"
  },

  {
    name: "Nintendo Switch 2",
    slug: "nintendo-switch-2",
    description:
      "任天堂新一代掌機主機，延續 Switch 的混合遊玩模式。"
  },

  {
    name: "PS5",
    slug: "ps5",
    description:
      "Sony 次世代家用主機，主打高畫質與沉浸式遊戲體驗。"
  },

  {
    name: "Xbox Series X",
    slug: "xbox-series-x",
    description:
      "Microsoft 高效能遊戲主機，支援 Game Pass 與 4K 遊戲。"
  }
];

export default function ThreeCPage() {

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
          3C Reviews
        </h1>

        <p className="mt-4 text-zinc-400">
          PulsePick 使用 AI 整理 YouTube、
          PTT、Dcard、Reddit 等平台的真實評價。
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">

          {tools.map((tool) => (

            <Link
              key={tool.slug}
              href={`/review/${tool.slug}`}
              className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-600 hover:bg-zinc-800"
            >

              <h2 className="text-2xl font-semibold">
                {tool.name}
              </h2>

              <p className="mt-3 text-zinc-400">
                {tool.description}
              </p>

            </Link>
          ))}

        </div>
      </div>
    </main>
  );
}