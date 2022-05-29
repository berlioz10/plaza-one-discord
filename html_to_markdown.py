def html_to_markdown(html):
    markdown = html.replace('<b>', '**').replace('</b>', '**')
    markdown = markdown.replace('<p>', '').replace('</p>', '')
    markdown = markdown.replace('<ul>', '').replace('</ul>', '')
    markdown = markdown.replace('<li>', '• ').replace('</li>', '')
    markdown = markdown.replace('&quot;', '"')
    
    return markdown