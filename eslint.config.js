import js from "@eslint/js";
import typescript from "typescript-eslint";

export default typescript.config(
  js.configs.recommended,
  ...typescript.configs.recommended,
  {
    files: ["src/frontend/**/*.ts"],
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname
      }
    },
    rules: {
      "max-lines": [
        "error",
        {
          max: 220,
          skipBlankLines: true,
          skipComments: true
        }
      ]
    }
  }
);
