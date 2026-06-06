import { ImageResponse } from "next/og";
import { NextRequest } from "next/server";

export const runtime = "edge";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const name = searchParams.get("name") || "商品評價";

  return new ImageResponse(
    (
      <div
        style={{
          width: "1200px",
          height: "630px",
          background: "linear-gradient(135deg, #09090b 0%, #18181b 60%, #000 100%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          justifyContent: "center",
          padding: "80px",
          fontFamily: "sans-serif",
        }}
      >
        {/* Badge */}
        <div
          style={{
            background: "rgba(255,255,255,0.08)",
            border: "1px solid rgba(255,255,255,0.12)",
            borderRadius: "999px",
            padding: "8px 20px",
            color: "#a1a1aa",
            fontSize: "20px",
            marginBottom: "32px",
            display: "flex",
          }}
        >
          AI Review Report
        </div>

        {/* Product name */}
        <div
          style={{
            fontSize: name.length > 16 ? "64px" : "80px",
            fontWeight: "bold",
            color: "#ffffff",
            lineHeight: 1.1,
            marginBottom: "24px",
            display: "flex",
          }}
        >
          {name}
        </div>

        {/* Subtitle */}
        <div
          style={{
            fontSize: "28px",
            color: "#71717a",
            display: "flex",
          }}
        >
          PulsePick 整合多平台評價，AI 產生客觀口碑分析
        </div>

        {/* Brand */}
        <div
          style={{
            position: "absolute",
            bottom: "60px",
            right: "80px",
            fontSize: "32px",
            fontWeight: "bold",
            color: "#ffffff",
            display: "flex",
          }}
        >
          PulsePick
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
