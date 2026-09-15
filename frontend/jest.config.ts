import type { Config } from "jest";

const config: Config = {
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
  // Don't try to transform node_modules except these
  transformIgnorePatterns: [
    "/node_modules/(?!(next)/)",
  ],
};

export default config;
