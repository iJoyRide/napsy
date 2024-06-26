'use strict';

const { merge } = require('webpack-merge');

const common = require('./webpack.common.js');
const PATHS = require('./paths');

// Merge webpack configuration files
const config = (env, argv) =>
  merge(common, {
    entry: {
      popup: PATHS.src + '/popup.js',
      process: PATHS.src + '/process.js',
      scrape: PATHS.src + '/scrape.js',
      predict: PATHS.src + '/predict.js',
    },
    devtool: argv.mode === 'production' ? false : 'source-map',
  });

module.exports = config;
