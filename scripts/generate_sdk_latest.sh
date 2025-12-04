#!/bin/sh

# Run openapi cli command
openapi-generator-cli generate   -i http://localhost:8000/openapi.json   -g typescript-axios   -o ./sdk 2>/dev/null || echo "Error: openapi-generator-cli generate failed"

# Add export * from "./sdk" to index.ts
echo "export * from './sdk';" >> ./sdk/index.ts


