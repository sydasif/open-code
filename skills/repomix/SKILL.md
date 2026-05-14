---
name: repomix
description: Pack codebases into AI-friendly formats with repomix. Use when packaging local/remote repositories, compressing code with Tree-sitter, splitting large outputs, or configuring repomix output formats (XML, Markdown, JSON, Plain). Handles file selection, token counting, git context, and security checks.
---

# Repomix Skill

Pack your codebase into a single AI-friendly file. Repomix supports local directories, remote GitHub repos, glob patterns, stdin piping, compression, and multiple output formats.

## Core Workflows

### Pack Local Directory

```bash
repomix                         # current directory
repomix path/to/directory      # specific directory
repomix --include "src/**/*.ts,**/*.md"
repomix --ignore "**/*.log,tmp/"
```

### Pack Remote Repository

```bash
repomix --remote https://github.com/user/repo
repomix --remote user/repo                    # shorthand
repomix --remote user/repo --remote-branch main
repomix --remote user/repo --remote-branch 935b695
```

### Pack via Stdin (file list)

```bash
find src -name "*.ts" -type f | repomix --stdin
git ls-files "*.ts" | repomix --stdin
rg --files --type ts | repomix --stdin
fzf -m | repomix --stdin
echo -e "src/index.ts\nsrc/utils.ts" | repomix --stdin
```

### Output Formats

| Flag               | Format   | Use Case                              |
| ------------------ | -------- | ------------------------------------- |
| `--style xml`      | XML      | Default — AI-optimized with XML tags  |
| `--style markdown` | Markdown | Human-readable, easy to scan          |
| `--style json`     | JSON     | Programmatic parsing, API integration |
| `--style plain`    | Plain    | Simple text with separators           |

```bash
repomix --style markdown -o output.md
repomix --style json -o output.json
repomix --stdout > custom-output.txt          # write to stdout
```

### Compression

Use Tree-sitter to extract code structure (classes, functions, interfaces) and reduce token count by ~70%:

```bash
repomix --compress
repomix --remote user/repo --compress
```

### Split Output for Large Codebases

Split into multiple files when AI tools have size limits (e.g., 1MB):

```bash
repomix --split-output 1mb
# Generates: repomix-output.1.xml, repomix-output.2.xml, ...
```

Size units: `500kb`, `1mb`, `2mb`, `1.5mb`, etc.

### Token Counting

```bash
repomix --token-count-tree            # show all files with token counts
repomix --token-count-tree 1000      # only files with 1000+ tokens
```

### Git Context

```bash
repomix --include-logs                          # last 50 commits
repomix --include-logs --include-logs-count 10 # specific count
repomix --include-diffs                        # working tree + staged diffs
```

### Other Useful Flags

| Flag                         | Description                              |
| ---------------------------- | ---------------------------------------- |
| `--copy`                     | Copy output to clipboard                 |
| `--remove-comments`          | Strip code comments before packing       |
| `--remove-empty-lines`       | Compact output                           |
| `--output-show-line-numbers` | Prefix each line with line number        |
| `--parsable-style`           | Escape XML/Markdown special chars        |
| `--no-security-check`        | Skip Secretlint scan                     |
| `--verbose`                  | Detailed debug output                    |
| `--quiet`                    | Suppress all except errors               |
| `--init`                     | Create repomix.config.json with defaults |

## Configuration

Create a config file:

```bash
repomix --init                    # local config
repomix --init --global           # global config (~/.config/repomix/)
```

### JSON Config Example

```json
{
  "$schema": "https://repomix.com/schemas/latest/schema.json",
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml",
    "compress": false,
    "removeComments": false,
    "removeEmptyLines": false
  },
  "include": ["**/*"],
  "ignore": {
    "useGitignore": true,
    "useDefaultPatterns": true,
    "customPatterns": ["**/*.log", "tmp/**"]
  },
  "security": {
    "enableSecurityCheck": true
  }
}
```

## Workflow Selection Guide

| Task                        | Command Pattern                          |
| --------------------------- | ---------------------------------------- | ---------------- |
| Quick pack current dir      | `repomix`                                |
| Pack specific files         | `repomix --include "src/**/*.ts"`        |
| Pack remote + compress      | `repomix --remote user/repo --compress`  |
| Filtered pack via file list | `<command>                               | repomix --stdin` |
| Large repo split output     | `repomix --compress --split-output 1mb`  |
| Analyze token distribution  | `repomix --token-count-tree 500`         |
| Include git history         | `repomix --include-logs --include-diffs` |
| Quick look at remote        | `repomix --remote user/repo --stdout`    |

## Security

Repomix runs Secretlint automatically to detect API keys, passwords, and other secrets. To disable:

```bash
repomix --no-security-check
```

Or in config:

```json
"security": { "enableSecurityCheck": false }
```

## MCP Tools

When repomix runs as an MCP server (`repomix --mcp`), these tools are available:

- **pack_codebase**: Package local directory — params: `directory`, `compress`, `includePatterns`, `ignorePatterns`, `topFilesLength`
- **attach_packed_output**: Attach existing output file — params: `path`, `topFilesLength`
- **pack_remote_repository**: Pack remote GitHub repo — params: `remote`, `compress`, `includePatterns`, `ignorePatterns`, `topFilesLength`
- **read_repomix_output**: Read output with line range — params: `outputId`, `startLine`, `endLine`
- **grep_repomix_output**: Search with JS RegExp — params: `outputId`, `pattern`, `contextLines`, `ignoreCase`
- **file_system_read_file**: Read with Secretlint security scan
- **file_system_read_directory**: List directory contents

## Tips

- Use `--stdout` to pipe output directly into another tool (e.g., `llm` CLI)
- Combine `--compress` with `--include` for large repos to stay within context limits
- Use `--parsable-style` when output contains code that breaks XML/Markdown formatting
- The `--stdin` option respects normal include/ignore patterns — piped files are filtered normally
