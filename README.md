# Public Reusable Workflows

This folder contains publicly available and safe-to-use GitHub reusable workflows.

## Example Consumer Workflow

```yaml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  ci:
    uses: Pinehood/ph-reusable-workflows/.github/workflows/node-ci.yml@main
    secrets: inherit
    with:
      ecr_repository: "ph-repo-name"
```
