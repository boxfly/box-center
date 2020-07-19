// config.js 
exports.config = { age:11};
// test.js
var config = require('./config.js').config;
console.log(config)