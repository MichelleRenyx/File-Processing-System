module.exports = {
  presets: [
    '@babel/preset-env',  // 处理 ES6+ 语法
    '@babel/preset-react', // 处理 JSX 语法
  ],
  plugins: [
    '@babel/plugin-transform-runtime', // 用于优化代码
  ],
};