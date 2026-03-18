# rushitnshah.github.io

Personal website at [rushitnshah.com](https://rushitnshah.com).

## Writing a blog post

1. Create a new file in `blog/posts/src/` named `YYYY-MM-DD-slug.md`:

   ```
   ---
   title: Your Title
   date: 2026-04-01
   description: One line summary shown in the post listing.
   ---

   Post body in Markdown.
   ```

2. Run the build script from the repo root:

   ```
   python3 build_blog.py
   ```

   This generates `blog/posts/YYYY-MM-DD-slug.html` and updates `blog/index.html`.

3. Commit both the source and generated files:

   ```
   git add blog/
   git commit -m "Add blog post: your title"
   ```

## Local preview

```
python3 -m http.server 8000
```

Then open `http://localhost:8000`. Hard-refresh (`Ctrl+Shift+R`) if styles look stale.
