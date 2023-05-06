module.exports = {
  // other webpack configuration options
  // ...
  module: {
    rules: [
      // other rules
      // ...
      {
        test: /\.svg$/,
        use: ['@svgr/webpack'],
      },
    ],
  },
  // ...
};