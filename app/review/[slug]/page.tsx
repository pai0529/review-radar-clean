import type { Metadata } from "next";
import ReviewClient from "./ReviewClient";

function fromSlug(slug: string) {
  return decodeURIComponent(slug).replace(/-/g, " ");
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {

  const { slug } = await params;

  const productName = fromSlug(slug);

  return {
    title: `${productName} AI 評價分析 | ReviewRadar`,
    description: `查看 ${productName} 的 AI 評價分析、優缺點、YouTube 留言整理與購買建議。`,
  };
}

export default async function ReviewPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {

  const { slug } = await params;

  return <ReviewClient slug={slug} />;
}