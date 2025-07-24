/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  trailingSlash: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:8000/api/:path*",
      },
      {
        source: "/callback",
        destination: "http://127.0.0.1:8000/callback",
      },
      {
        source: "/health",
        destination: "http://127.0.0.1:8000/health",
      },
    ]
  },
}

module.exports = nextConfig
