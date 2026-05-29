import Link from "next/link";

const tools = [
  {
    name: "ChatGPT",
    slug: "chatgpt",
    description:
      "最熱門的 AI 聊天與生產力工具。"
  },

  {
    name: "Claude",
    slug: "claude",
    description:
      "擅長長文本與程式理解的 AI 助手。"
  },

  {
    name: "Gemini",
    slug: "gemini",
    description:
      "Google 推出的 AI 模型與助手。"
  },

  {
    name: "Notion AI",
    slug: "notion-ai",
    description:
      "整合在 Notion 內的 AI 生產力工具。"
  },

  {
    name: "Cursor",
    slug: "cursor",
    description:
      "AI 程式開發編輯器。"
  }
];

export default function AIToolsPage() {

  return (
    <main className="min-h-screen bg-black px-6 py-16 text-white">

      <div className="mx-auto max-w-5xl">

        <h1 className="text-5xl font-bold">
          AI Tools Reviews
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