import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import eslintConfigPrettier from "eslint-config-prettier";

// jsx-a11y + typescript-eslint: eslint-config-next (core-web-vitals / typescript)
// zaten kayıtlı. Aynı plugin'i ikinci kez eklemek ConfigError verir.
// Paketler package.json'da açık bağımlılık olarak durur.
const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  eslintConfigPrettier,
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    "playwright-report/**",
    "test-results/**",
    "e2e/**",
  ]),
]);

export default eslintConfig;
