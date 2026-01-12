# Install OLAF

This page provides copy/paste commands to install OLAF into your repository.

## Windows (PowerShell)

Run from your repo root:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -Command "iwr -useb https://raw.githubusercontent.com/haal-ai/haal-ide/main/.olaf/tools/init-olaf.ps1 | iex"
```

## Linux (bash/sh)

Run from your repo root:

```sh
curl -fsSL https://raw.githubusercontent.com/haal-ai/haal-ide/main/.olaf/tools/init-olaf.sh | sh
```

## macOS (zsh)

Run from your repo root:

```zsh
curl -fsSL https://raw.githubusercontent.com/haal-ai/haal-ide/main/.olaf/tools/init-olaf.zsh | zsh
```
