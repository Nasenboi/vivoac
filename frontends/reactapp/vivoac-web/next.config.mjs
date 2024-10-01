/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  trailingSlash: false,
  images: {
    domains: ["localhost"],
  },
};

export default nextConfig;
