def split_into_chapters(text):
    chapters = text.split('Chapter ')
    return ['Chapter ' + chapter for chapter in chapters if chapter.strip()]
