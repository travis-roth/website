#!/usr/bin/env python3
"""Render the Jinja templates in templates/ to a static site in dist/.

Every former Flask route becomes <path>/index.html so the URLs stay the same
(/projects, /weather_home, ...). The one dynamic feature, the weather lookup,
is done in the browser against the shared API at kiln-api.travisroth.dev.

    pip install -r requirements.txt && python3 build.py
"""
import pathlib
import shutil

from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"

# url path -> template
PAGES = {
    "/": "index.html",
    "/projects": "projects.html",
    "/policy": "policy.html",
    "/dubgrub": "dubgrub.html",
    "/bloodworks": "bloodworks.html",
    "/billionaires": "billionaires.html",
    "/edfr": "edfr.html",
    "/website": "website.html",
    "/weather_home": "weather_proj/weather_home.html",
    "/weather": "weather_proj/weather.html",
}


def url_for(endpoint, filename=None, **_):
    """Flask-compatible url_for for the one case the templates use."""
    if endpoint == "static":
        return "/static/" + filename
    raise ValueError("url_for(%r) is not supported in the static build" % endpoint)


def main():
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)
    env.globals["url_for"] = url_for

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST / "static")

    for path, template in PAGES.items():
        out = DIST / "index.html" if path == "/" else DIST / path.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(env.get_template(template).render(), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))

    # Render serves 404.html for unknown paths on static sites.
    not_found = env.get_template("base.html").render().replace(
        "<main>",
        '<main><section class="weather"><h1>Page not found</h1><p><a href="/">Back home</a></p></section>',
        1,
    )
    (DIST / "404.html").write_text(not_found, encoding="utf-8")
    print("wrote dist/404.html")


if __name__ == "__main__":
    main()
