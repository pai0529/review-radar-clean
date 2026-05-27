import type { Metadata } from "next";
import ReviewClient from "./ReviewClient";

type Props = {
  params: Promise<{
    slug: string;
  }>;
};

function fromSlug(slug: string) {
  return decodeURIComponent(slug).replace(/-/g, " ");
}

export async function generateMetadata({
  params,
}: Props): Promise<Metadata> {
  const { slug } = await params;
  const productName = fromSlug(slug);

  return {
    title: `${productName} 評價總整理｜PulsePick`,
    description: `PulsePick 使用 AI 整理 YouTube、PTT、Dcard、Reddit、Mobile01 等平台的 ${productName} 真實評價、優缺點與購買建議。`,
    openGraph: {
      title: `${productName} 評價總整理｜PulsePick`,
      description: `AI 整理 ${productName} 的全網評價與真實口碑。`,
      type: "website",
    },
  };
}

export default async function Page({ params }: Props) {
  const { slug } = await params;
  return <ReviewClient slug={slug} />;
}