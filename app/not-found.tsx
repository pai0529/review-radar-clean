export default function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-zinc-950 via-zinc-900 to-black px-6 text-white">
      <div className="text-center">
        <p className="text-sm text-zinc-500">404</p>
        <h1 className="mt-4 text-5xl font-bold">找不到頁面</h1>
        <p className="mt-4 text-zinc-400">這個頁面不存在，或是連結已失效。</p>
        <a
          href="/"
          className="mt-8 inline-block rounded-2xl bg-white px-8 py-4 font-bold text-black transition hover:bg-zinc-200"
        >
          回首頁搜尋
        </a>
      </div>
    </main>
  );
}
