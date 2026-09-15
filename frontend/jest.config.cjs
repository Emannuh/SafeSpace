/** @type {import('jest').Config} */
const config = {
  preset: "ts-jest",
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],
  moduleNameMapper: {
    // Handle @/ path alias
    "^@/(.*)$": "<rootDir>/$1",
    // Handle CSS imports (not needed in tests)
    "^.+\\.css$": "<rootDir>/__mocks__/styleMock.js",
  },
  transform: {
    "^.+\\.(ts|tsx)$": ["ts-jest", {
      tsconfig: {
        jsx: "react-jsx",
      },
    }],
  },
  testMatch: ["**/__tests__/**/*.test.{ts,tsx}"],
  transformIgnorePatterns: [
    "/node_modules/(?!(next)/)",
  ],
};

module.exports = config;
