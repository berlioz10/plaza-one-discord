import urllib.parse
import re

def html_to_markdown(html):
    print(html)
    markdown = urllib.parse.unquote(html)
    markdown = markdown.replace('<b>', '**').replace('</b>', '**')
    markdown = markdown.replace('<strong>', '**').replace('</strong>', '**')
    markdown = markdown.replace('<em>', '_').replace('</em>', '_')
    markdown = markdown.replace('<p>', '').replace('</p>', '')
    markdown = markdown.replace('<ul>', '').replace('</ul>', '')
    markdown = markdown.replace('<li>', '• ').replace('</li>', '')
    markdown = markdown.replace('&quot;', '"')
    markdown = markdown.replace('&gt;', '>')
    
    markdown = re.sub('<a href=\"(.+)\">(.+)</a>', "[\\2](\\1)", markdown)
    print(markdown)
    
    return markdown