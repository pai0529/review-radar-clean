import type { Metadata } from "next";
import ReviewClient from "./ReviewClient";

function fromSlug(slug: string) {
  return decodeURIComponent(slug).replace(/-/g, " ");
}

export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {

  const productName = fromSlug(params.slug);

  return {
    title: `${productName} AI 評價分析 | ReviewRadar`,
    description: `查看 ${productName} 的 AI 評價分析、優缺點、YouTube 留言整理與購買建議。`,
  };
}

export default function ReviewPage({
  params,
}: {
  params: { slug: string };
}) {
  return <ReviewClient slug={params.slug} />;
}