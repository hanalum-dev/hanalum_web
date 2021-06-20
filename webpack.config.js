var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
  context: __dirname,
  // mode: 'production',
  mode: 'development',
  entry: {
    AppJohaApplyFormWizard: './public/js/AppJohaApplyFormWizard.js',
  },
  output: {
      path: path.resolve('./assets/bundles/'),
      filename: "[name]-[hash].js",
  },
  devServer: {
    hot: true,
    proxy: {
      contentBase: './assets/bundles/',
      '!/static/bundles/**': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new VueLoaderPlugin()
  ],
  module : {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          hotReload: true,
        }
      },
      {
        test: /\.css/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              url: false,
              sourceMap: true,
            },
          },
        ],
      },
    ]
  },

  resolve: {
    alias: {
      'vue': path.resolve('./node_modules/vue/dist/vue.js'),
    }
  },
}