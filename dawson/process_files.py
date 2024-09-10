import dotenv
import re

def split_dawson_legal(src: list[str], title=None)->list[str]:
    article_pattern = '^ARTICLE\s+([IVX]+)\s*\n'
    section_pattern1 = '^(\d[0-9\.]+)\s(.*?)\n'
    section_pattern2 = '^Section\s+(\d[0-9\.]+)\s+(.*)\n'
    section_pattern = f"({section_pattern1}|{section_pattern2})"
    para_pattern = '^\\s*\(([a-z])\)\\s*(.*)'

    def do_section():
        nonlocal section_lines, curr_article, curr_article_title
        nonlocal curr_section, segs, curr_para
        # save current section lines with prefixed article/section
        frag = " ".join(section_lines).strip()
        if len(frag) > 0:
            title_frag = '' if title is None else f"{title}: "
            article_frag = '' if curr_article is None else f"Article {curr_article}"
            section_frag = '' if curr_section is None else f" : Section {curr_section}"
            para_frag = '' if curr_para is None else f": paragraph {curr_para}"
            if m := re.search(f"^\(.*?\)(.*)", frag):
                frag = m.group(1).strip()
            s = f"{title_frag}{article_frag}{section_frag}{para_frag}: {frag}"
            segs.append(s)
        section_lines = []

    curr_article = None
    curr_section = None
    curr_para = None

    line_cnt = 0
    segs = [] if title is None else [title]
    section_lines = []
    curr_article_title = None
    curr_article = None
    curr_section = None
    while True:
        if line_cnt >= len(src) - 1:
            do_section() # flush anything left at end
            break
        line = src[line_cnt]
        line_cnt += 1

        if m := re.search(article_pattern, line):
            do_section()
            curr_article = m.group(1)   
            # Use next line as article title
            curr_article_title = src[line_cnt].strip()
            line_cnt += 1
            curr_section = None
            curr_para = None
            continue

        # We have 2 patterns for sections; try both
        m = re.search(section_pattern1, line)
        m = m if not m is None else re.search(section_pattern2, line)
        if m:
            do_section()
            # parse group 2 to separate section title from rest of line.
            section_lines = [m.group(2).strip()]
            curr_section = m.group(1)
            curr_para = None
            continue

        if m := re.search(para_pattern, line):
            do_section()
            # parse group 2 to separate section title from rest of line.
            section_lines = [line.strip()]
            curr_para = m.group(1)
            continue

        x = line.strip()
        if len(x) > 0: section_lines.append(x)
    return segs

def split_bylaws():
    with open('dawson/dawson_bylaws.txt', 'r') as f:
        lines = f.readlines()
        split = split_dawson_legal(lines, "BYLAWS")
        for i, s in enumerate(split):
            with open(f'dawson/rag_files/bylaws/bylaws-{i}.txt', 'w') as r:
                r.write(s)
    return split

def split_covenants():
    with open('dawson/dawson_covenants-2005.txt', 'r') as f:
        lines = f.readlines()
        split = split_dawson_legal(lines, "COVENANTS")
    for i, s in enumerate(split):
        with open(f'dawson/rag_files/covenants/covenants-{i}.txt', 'w') as r:
            r.write(s)
    return split

def test_splitter():
    src = ["line with split word-", "at the end."]
    split = split_dawson_legal(src)

dotenv.load_dotenv()
bylaws_split = split_bylaws()
covenants_split = split_covenants()

print("Done")