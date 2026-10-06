"""Add stable subheading links and an on-page navigation rail to help articles."""
import html
import re


def add_page_navigation(text):
    main=re.search(r'<main\b[^>]*>.*?</main>',text,re.S)
    if not main or 'wiki-directory' in main[0]: return text
    content=main[0]
    used=set(re.findall(r'\bid="([^"]+)"',text))
    headings=[]
    def heading(match):
        tag,attrs,label=match.groups()
        title=html.unescape(re.sub('<[^>]+>','',label)).strip()
        existing=re.search(r'\bid="([^"]+)"',attrs)
        if existing: anchor=existing[1]
        else:
            stem=re.sub('[^a-z0-9]+','-',title.lower()).strip('-') or 'section'
            anchor=stem;number=2
            while anchor in used: anchor=f'{stem}-{number}';number+=1
            used.add(anchor);attrs+=f' id="{anchor}"'
        headings.append((tag,anchor,title))
        return f'<{tag}{attrs}>{label}</{tag}>'
    content=re.sub(r'<(h[23])([^>]*)>(.*?)</\1>',heading,content,flags=re.S)
    text=text[:main.start()]+content+text[main.end():]
    if not headings:return text
    links=''.join(f'<a href="#{anchor}"'+(' class="toc-subheading"' if tag=='h3' else '')+f'>{html.escape(title)}</a>' for tag,anchor,title in headings)
    toc='<aside class="wiki-page-toc"><details class="wiki-page-sections" open><summary>On this page</summary><nav aria-label="On this page">'+links+'</nav></details></aside>'
    return text.replace('class="wiki-layout"','class="wiki-layout with-page-toc"',1).replace('</main></div>','</main>'+toc+'</div>',1)
