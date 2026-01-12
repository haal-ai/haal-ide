# Example: Using `fix-code-smells` on a Go helper (syncer.DownloadDir)

This example shows how to use the `fix-code-smells` skill in **Evolution/Refactoring Mode**
(on existing code) against a small Go helper function in the OLAF CLI.

## Context

- **Codebase**: `.olaf/core/scripts/olaf`
- **File**: `internal/syncer/syncer.go`
- **Function**: `DownloadDir`
- **Goal**: Check for maintainability issues and potential refactors *without*
  changing public behavior or APIs.

## Target Function

```go
func DownloadDir(r Repo, srcPath, dst, token string) error {
    entries, err := githubx.ListDir(githubx.Repo{Owner: r.Owner, Name: r.Name}, srcPath, r.Branch, token)
    if err != nil {
        return err
    }
    if err := os.MkdirAll(dst, 0o755); err != nil {
        return err
    }
    for _, e := range entries {
        target := filepath.Join(dst, e.Name)
        switch e.Type {
        case "file":
            b, err := githubx.GetRaw(githubx.Repo{Owner: r.Owner, Name: r.Name}, e.Path, r.Branch, token)
            if err != nil {
                return err
            }
            if err := os.MkdirAll(filepath.Dir(target), 0o755); err != nil {
                return err
            }
            if err := os.WriteFile(target, b, 0o644); err != nil {
                return err
            }
        case "dir":
            if err := DownloadDir(r, e.Path, target, token); err != nil {
                return err
            }
        }
    }
    return nil
}
```

## How `fix-code-smells` should reason (Evolution Mode)

- Treat the current behavior and signature of `DownloadDir` as **frozen**.
- Focus checks on:
  - Single responsibility and function size (short, focused helper).
  - Naming clarity (`DownloadDir`, `srcPath`, `dst`, `target`).
  - Control flow and error handling.
  - Testability (hard-wired dependencies vs injectable seams).

### Example Analysis Summary

- Function is already **short and focused**: downloads a directory tree from a
  GitHub repo into a local directory.
- Naming is clear; branching by `e.Type` is easy to follow.
- Main smells are **testability** and **small duplication**:
  - Direct use of `githubx.ListDir` / `githubx.GetRaw` and `os` functions makes
    isolated unit testing harder.
  - The `githubx.Repo{Owner: r.Owner, Name: r.Name}` literal is duplicated.

### Example Refactor Suggestions (Public API unchanged)

1. **Small readability cleanup**

   Introduce a local `repo` variable to avoid repeating the struct literal:

   ```go
   func DownloadDir(r Repo, srcPath, dst, token string) error {
       repo := githubx.Repo{Owner: r.Owner, Name: r.Name}

       entries, err := githubx.ListDir(repo, srcPath, r.Branch, token)
       if err != nil {
           return err
       }
       if err := os.MkdirAll(dst, 0o755); err != nil {
           return err
       }
       for _, e := range entries {
           target := filepath.Join(dst, e.Name)
           switch e.Type {
           case "file":
               b, err := githubx.GetRaw(repo, e.Path, r.Branch, token)
               if err != nil {
                   return err
               }
               if err := os.MkdirAll(filepath.Dir(target), 0o755); err != nil {
                   return err
               }
               if err := os.WriteFile(target, b, 0o644); err != nil {
                   return err
               }
           case "dir":
               if err := DownloadDir(r, e.Path, target, token); err != nil {
                   return err
               }
           }
       }
       return nil
   }
   ```

2. **(Optional) Testability seam for future work**

   For a deeper refactor, still in Evolution Mode, you can introduce small
   interfaces (e.g. `gitFSClient`, `FS`) and an internal helper
   `downloadDirWith(...)` to allow unit tests to inject fakes, while keeping the
   exported `DownloadDir` function as a thin wrapper.

## Takeaways for Users

- `fix-code-smells` is not only for big rewrites; it can validate that a small
  helper is already healthy and highlight **where not to change things**.
- In Evolution Mode, the skill focuses on **internal quality** (readability,
  SRP, DI, testability) while **preserving public APIs and behavior**.
- For well-structured helpers like `DownloadDir`, the main outcome may be a
  confirmation that the function is fine plus a few low-risk improvements.
