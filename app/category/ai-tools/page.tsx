import Link from "next/link";

const tools = [
  { name: "ChatGPT", slug: "chatgpt", domain: "openai.com", description: "最熱門的 AI 聊天與生產力工具。" },
  { name: "Claude", slug: "claude", domain: "anthropic.com", description: "擅長長文本與程式理解的 AI 助手。" },
  { name: "Gemini", slug: "gemini", domain: "gemini.google.com", description: "Google 推出的 AI 模型與助手。" },
  { name: "Notion AI", slug: "notion-ai", domain: "notion.so", description: "整合在 Notion 內的 AI 生產力工具。" },
  { name: "Cursor", slug: "cursor", domain: "cursor.com", description: "AI 程式開發編輯器。" },
];

function faviconUrl(domain: string) {
  return `https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://${domain}&size=256`;
}

export default function AIToolsPage() {
  return (
    <main className="min-h-screen bg-black px-6 py-16 text-white">
      <div className="mx-auto max-w-5xl">

        <a href="/" className="text-sm text-zinc-400 hover:text-white">← 回首頁</a>

        <h1 className="mt-8 text-5xl font-bold">AI Tools Reviews</h1>
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
