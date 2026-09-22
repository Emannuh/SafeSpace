import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Standalone output for container/Railway deployment
  output: "standalone",

  // Ensure the API base URL is not baked in at build time for flexibility.
  // NEXT_PUBLIC_API_BASE_URL must be set as an environment variable.
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL ?? "",
  },
};

export default nextConfig;
