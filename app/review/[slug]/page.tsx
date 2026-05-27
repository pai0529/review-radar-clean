import { Metadata } from "next";
import ReviewClient from "./ReviewClient";

type Props = {
  params: Promise<{
    slug: string;
  }>;
};

export async function generateMetadata(
  { params }: Props
): Promise<Metadata> {

  const { slug } = await params;

  const productName = slug
    .replace(/-/g, " ");

  const title =
    `${productName} 評價總整理｜PulsePick`;

  const description =
    `AI 整理 YouTube、PTT、Dcard、Reddit 等平台的 ${productName} 真實評價與優缺點分析。`;

  return {
    title,
    description,

    openGraph: {
      title,
      description,
      type: "website",
    },

    twitter: {
      card: "summary_large_image",
      title,
      description,
    },
  };
}

export default async function Page(
  { params }: Props
) {

  const { slug } = await params;

  return (
    <ReviewClient slug={slug} />
  );
}