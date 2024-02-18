/** @type {import('next').NextConfig} */
const { i18n } = require("./next-i18next.config");

module.exports = {
  output: "standalone",
  reactStrictMode: true,
  i18n,
  swcMinify: true,
  experimental: {
    largePageDataBytes: 512 * 100000,
  },
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: true
  }
};
