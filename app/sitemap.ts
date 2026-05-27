import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {

  const baseUrl =
    "https://review-radar-clean-delta.vercel.app";

  const reviewPages = [
    "chatgpt",
    "tiktok",
    "iphone-15",
    "steam-deck"
  ];

  const reviewRoutes = reviewPages.map((slug) => ({
    url: `${baseUrl}/review/${slug}`,
    lastModified: new Date(),
    changeFrequency: "daily" as const,
    priority: 0.8,
  }));

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },

    ...reviewRoutes
  ];
}