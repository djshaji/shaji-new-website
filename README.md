# Shaji Khan’s portfolio

A five-page Bootstrap 5.3.3 website with Lucide 0.468.0 icons. Bootstrap, Lucide, Geist, and the editorial cover artwork are included locally. Browsing the site requires no CDN, build tool, or server runtime. The artwork is illustrative.

| Page | Source | Deployable file |
| --- | --- | --- |
| Home | `content/index.md` | `dist/index.html` |
| Music | `content/music.md` | `dist/music.html` |
| Code | `content/code.md` | `dist/code.html` |
| Research | `content/research.md` | `dist/research.html` |
| Travel | `content/travel.md` | `dist/travel.html` |

## Build and preview

From the repository checkout, install the build dependencies and generate the five pages.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 build.py
```

Serve the compiled site locally, then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

## Edit the site

Edit the Markdown files in `content/`. The top of each file sets its page title, introduction, and sidebar details. Set the default palette (`slate`, `ocean`, `forest`, `rose`, or `warm`) and light or dark mode in `site.yaml`. Visitors can change both in the navigation. Edit styles in `assets/site.css`.

Run `python3 build.py` after editing. The build regenerates `dist/` from the source files.

## Publish with Apache

Upload the **contents of `dist/`** to the desired Apache document root or public subdirectory. The page and asset links use relative paths. Keep the editable project outside the document root. Disable directory listings for the destination and serve it through your HTTPS virtual host. Open the destination and follow each navigation link after uploading.

For GitHub source control, commit the source Markdown, configuration, builder, requirements, and assets. The `dist/` directory can be rebuilt from those files.
