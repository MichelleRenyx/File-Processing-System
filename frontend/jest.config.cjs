module.exports = {
    testEnvironment: 'jsdom',
    transform: {
      '^.+\\.jsx?$': 'babel-jest',
    },
    transformIgnorePatterns: [
      '/node_modules/(?!your-esm-package-name|other-package-name).+\\.js$',
    ],
    testMatch: [
      '<rootDir>/src/**/*.test.js',
      '<rootDir>/src/**/*.spec.js',
    ],
    collectCoverageFrom: [
      'src/**/*.{js,jsx}',
      '!src/index.js',
    ],
    coverageDirectory: './coverage',
    coverageReporters: ['text', 'lcov', 'json'],
    setupFilesAfterEnv: [
      '@testing-library/jest-dom',
    ],
    globals: {
      'process.env': {
        NODE_ENV: 'test',
      },
    },
    moduleNameMapper: {
      '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    },
    modulePaths: [
      '<rootDir>/src/',
    ],
    testTimeout: 10000,
  };