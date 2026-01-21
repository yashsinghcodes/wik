#!/usr/bin/env python3
import os
import sys
import textwrap
import pydoc
import hashlib

from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

try:
    width, height = os.get_terminal_size()
    p = True
except OSError:
    width = 120
    height = 80
    p = False


# Some ANSI escape color codes
class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


_DEFAULT_HEADERS = {
    "User-Agent": "wik/1.4.0 (https://github.com/yashsinghcodes/wik)",
    "Accept": "text/html",
    "Accept-Language": "en",
}

_cache_enabled = True


def _use_tty():
    return p and sys.stdout.isatty()


def _section_heading(text, level=2):
    indent = "" if level == 2 else "  " if level == 3 else "    "
    label = text.upper() if level in (2, 3, 4) else text
    if _use_tty():
        label = color.BOLD + label + color.END
    return indent + label


def _title_block(title, link=None):
    lines = []
    title_line = title.upper()
    if _use_tty():
        title_line = color.BOLD + title_line + color.END
    lines.append(title_line)
    lines.append("")
    lines.append(_section_heading("NAME", level=2))
    lines.append("    " + title + " - Wikipedia article")
    if link:
        lines.append("")
        lines.append(_section_heading("SOURCE", level=2))
        lines.append("    " + link)
    lines.append("")
    return lines


def _should_page(text):
    return text.count("\n") > height - 5 or len(text) > 2000


def _emit(lines, force_page=False):
    text = "\n".join(lines).rstrip() + "\n"
    if _use_tty() and (force_page or _should_page(text)):
        pydoc.pager(text)
        return
    print(text, end="")


def _collect_blocks(soup):
    blocks = []
    containers = soup.select("div.mw-parser-output")
    if containers:
        root = max(
            containers,
            key=lambda el: len(el.find_all(["p", "h2", "h3", "h4", "h5"])),
        )
    else:
        root = soup
    for el in root.find_all(["p", "h2", "h3", "h4", "h5"]):
        if el.name == "p":
            blocks.append({"type": "para", "el": el})
            continue
        headline = el.find("span", class_="mw-headline")
        if headline:
            blocks.append(
                {"type": "heading", "el": headline, "level": int(el.name[1])}
            )
            continue
        heading_text = el.get_text(" ", strip=True).replace("[edit]", "").strip()
        if heading_text:
            blocks.append(
                {
                    "type": "heading",
                    "el": el,
                    "level": int(el.name[1]),
                    "text": heading_text,
                }
            )
    return blocks


def _skip_para(text):
    lowered = text.lower()
    return any(
        phrase in lowered
        for phrase in [
            "this is an accepted version of this page",
            "accepted version of this page",
            "this article is about",
            "for other uses",
        ]
    )


def _format_paragraph(text, indent=4):
    pad = " " * indent
    wrapped = textwrap.fill(text, width=width, initial_indent=pad, subsequent_indent=pad)
    return wrapped.splitlines()


def _cache_dir():
    base = os.environ.get("XDG_CACHE_HOME")
    if not base:
        if os.name == "nt":
            base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        elif sys.platform == "darwin":
            base = os.path.join(os.path.expanduser("~"), "Library", "Caches")
        else:
            base = os.path.join(os.path.expanduser("~"), ".cache")
    cache_root = os.path.join(base, "wik")
    os.makedirs(cache_root, exist_ok=True)
    return cache_root


def _cache_path(term, lang):
    key = f"{lang}:{term}".encode("utf-8")
    digest = hashlib.sha256(key).hexdigest()
    return os.path.join(_cache_dir(), f"{digest}.html")


def set_cache_enabled(enabled):
    global _cache_enabled
    _cache_enabled = bool(enabled)


def clear_cache():
    cache_root = _cache_dir()
    removed = 0
    for name in os.listdir(cache_root):
        path = os.path.join(cache_root, name)
        if os.path.isfile(path):
            os.remove(path)
            removed += 1
    return removed

# Maybe Future Use
# def get_tags(d, params):
#   if any((lambda x:b in x if a == 'class' else b == x)(d.attrs.get(a, [])) for a, b in params.get(d.name, {}).items()):
#      yield d
#   for i in filter(lambda x:x != '\n' and not isinstance(x, bs4.element.NavigableString) , d.contents):
#    yield from get_tags(i, params)


# Makes request to wikipedia for the code
def req(term, lang="en"):
    global wikiurl
    term = term.replace(" ", "_")
    wikiurl = "https://" + lang + ".wikipedia.org/wiki/" + quote(term)
    if _cache_enabled and term.lower() != "special:random":
        cache_path = _cache_path(term, lang)
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as handle:
                cached = handle.read()
            if cached:
                return cached
    r = requests.get(wikiurl, timeout=15, headers=_DEFAULT_HEADERS)
    if r.status_code == 200 and "mw-parser-output" in r.text:
        if _cache_enabled and term.lower() != "special:random":
            with open(cache_path, "w", encoding="utf-8") as handle:
                handle.write(r.text)
        return r.text
    rest_url = "https://" + lang + ".wikipedia.org/api/rest_v1/page/html/" + quote(term)
    r2 = requests.get(rest_url, timeout=15, headers=_DEFAULT_HEADERS)
    if r2.status_code == 200:
        if _cache_enabled and term.lower() != "special:random":
            with open(cache_path, "w", encoding="utf-8") as handle:
                handle.write(r2.text)
        return r2.text
    return r.text


# Gets summary
def getSummary(term, lang="en"):
    final_content = []
    content = req(term, lang)
    soup = BeautifulSoup(content, "html.parser")
    content = soup.find_all("p")
    lines = _title_block(str(term), link=str(wikiurl))
    lines.append(_section_heading("SUMMARY", level=2))
    lines.append("")
    last_item = None
    for i in content:
        last_item = i
        # Removing all empty lines
        if i.get_text() == "\n":
            continue
        # Removing all external links from the article
        if i("sup"):
            for tag in i("sup"):
                tag.decompose()

        data = i.get_text().strip()
        final_content.append(data)
        if len(final_content) == 3:
            break  # Breaks after 3 line of content

    # Search for other if not available
    if last_item is None:
        lines.append("No summary found.")
        _emit(lines, force_page=True)
        return
    if "Other reasons this message may be displayed" in str(last_item):
        lines.append("Did you mean:")
        _emit(lines)
        term = searchInfo(term, lang=lang, called=True)
    else:
        for idx, para in enumerate(final_content):
            lines.extend(_format_paragraph(para))
            if idx != len(final_content) - 1:
                lines.append("")
        _emit(lines)


def getInfo(term, lang="en"):
    final_content = []
    content = req(term, lang)
    soup = BeautifulSoup(content, "html.parser")
    content = _collect_blocks(soup)

    # content = soup.find_all(['p',['span', {'class':'mw-headline'}]])
    # content = soup.find_all(re.compile('p|span'), {'class':re.compile('|mw-headline')})#['p',('span' , {"class": "toctext"})])
    # content = list(get_tags(soup),{'p':{}, 'span':{'class': 'mw-headline'}})

    # Remove all external links
    for i in content:
        el = i["el"]
        if el("sup"):
            for tag in el("sup"):
                tag.decompose()

        data = el.get_text().strip()
        if not data:
            continue
        if i["type"] == "heading":
            text = i.get("text", data)
            final_content.append(
                {"type": "heading", "text": text, "level": i["level"]}
            )
        else:
            if _skip_para(data):
                continue
            final_content.append({"type": "para", "text": data})

    # Search if not found
    if final_content and "may refer to:" in final_content[0].get("text", ""):
        term = searchInfo(term, lang=lang)

    # Printing the output
    else:
        lines = _title_block(str(term), link=str(wikiurl))
        if not final_content:
            lines.append(_section_heading("CONTENT", level=2))
            lines.append("")
            lines.append("    No content found.")
            _emit(lines, force_page=True)
            return
        for i in final_content:
            if i["type"] == "heading":
                heading = i["text"]
                if heading in [
                    "See also",
                    "Notes",
                    "References",
                    "External links",
                    "Further reading",
                ]:
                    continue
                lines.append("")
                lines.append(_section_heading(heading, level=i["level"]))
                lines.append("")
                continue
            para = i["text"]
            if "Other reasons this message may be displayed:" in para:
                _emit(lines)
                searchInfo(term, lang=lang)
                return
            lines.extend(_format_paragraph(para))
            lines.append("")
        _emit(lines, force_page=True)


def getRand(lang="en"):
    """
    gerRand() retrieves a random article from Wikipedia.

    :@param term {string}: String name of article to retreive. Set to Special:Random to retreive random article.
    :@param lang {string}: Language to retreive article in.
    :@return     {string}: Returns formatted Wikipedia article string.
    """

    final_content = []

    # still use var term so we can use existing req() function
    term = "Special:Random"
    content = req(term, lang)
    soup = BeautifulSoup(content, "html.parser")
    content = []

    canonical = soup.find("link", rel="canonical")
    if canonical and canonical.get("href"):
        global wikiurl
        wikiurl = canonical.get("href")

    # get title of article and strip "- Wikipedia" and right whitespace
    for title in soup.find_all("title"):
        title = title.get_text().split("-", 1)
        title = title[0].rstrip()

    lines = _title_block(str(title), link=str(wikiurl))

    # Seprating section titles from the paragraphs
    content = _collect_blocks(soup)

    # Remove all external links
    for i in content:
        el = i["el"]
        if el("sup"):
            for tag in el("sup"):
                tag.decompose()

        data = el.get_text().strip()
        if not data:
            continue
        if i["type"] == "heading":
            text = i.get("text", data)
            final_content.append(
                {"type": "heading", "text": text, "level": i["level"]}
            )
        else:
            if _skip_para(data):
                continue
            final_content.append({"type": "para", "text": data})

    # Printing the output
    for i in final_content:
        if i["type"] == "heading":
            heading = i["text"]
            if heading in [
                "See also",
                "Notes",
                "References",
                "External links",
                "Further reading",
            ]:
                continue
            lines.append("")
            lines.append(_section_heading(heading, level=i["level"]))
            lines.append("")
            continue
        para = i["text"]
        if "Other reasons this message may be displayed:" in para:
            _emit(lines)
            searchInfo(term, lang=lang)
            return
        lines.extend(_format_paragraph(para))
        lines.append("")
    _emit(lines, force_page=True)


# Search for Similar Articles
def searchInfo(term, lang="en", called=False):
    # https://en.wikipedia.org/w/index.php?fulltext=Search&search
    r = requests.get(
        "https://" + lang + ".wikipedia.org/w/index.php",
        params={"fulltext": "Search", "search": term},
        timeout=15,
        headers=_DEFAULT_HEADERS,
    )
    if "/wiki/" in r.url:
        getInfo(term, lang=lang)
    else:
        content = r.text
        soup = BeautifulSoup(content, "html.parser")
        content = soup.find_all("a", {"data-serp-pos": True})
        dym = soup.find("em")
        lines = _title_block(term, link=str(r.url))
        lines.append(_section_heading("SEARCH RESULTS", level=2))
        lines.append("")
        if dym is not None:
            lines.append("    Did you mean: " + dym.get_text())
            lines.append("")
        if called is False and not content:
            lines.append("    No results found.")
        for i in content:
            title = i.get("title")
            if not title:
                continue
            lines.append("    " + title)
        _emit(lines, force_page=True)
