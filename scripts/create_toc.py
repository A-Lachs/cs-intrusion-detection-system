#!/usr/bin/env python3
"""
Automatically generate or update a clickable Table of Contents
for a Jupyter notebook (.ipynb) file.
NOTE: pip install nbformat
"""

import re
import sys
import nbformat

TOC_HEADER = "# Table of Contents"

def slugify(text):
    """
    Convert a heading string into a clean, predictable identifier (slug) 
    usable as anchor for links in jupyter notebooks/VS code.
    - Note: Keep numerical structure '2.1 Heading' by converting to '21-heading'. 
    """
    text = text.strip().lower()
    #text = re.sub(r"[^\w\s.-]", "", text)  # keep letters, numbers, spaces, and dots
    #text = re.sub(r"\s+", "-", text)       # spaces to hyphens
    
    text = re.sub(r"&[a-zA-Z0-9#]+;", "", text) # remove html entities
    text = text.replace(".", "")                # drop all dots
    text = re.sub(r"[^\w\s-]", "", text)        # remove all punctuation except spaces, hyphens, underscores
    text = re.sub(r"\s+", "-", text)            # convert whitespace to hyphens
    text = re.sub(r"-+", "-", text)             # collapse hyphens

    return text.strip("-")

def build_toc(nb):
    """
    Generate a markdown Table of Contents from a notebook object.

    Args:
        nb: A notebook object (from nbformat.read)

    Returns:
        str containing the TOC in markdown format.
    """
    headers = [] # list to store each TOC line

    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            # split cell contents to lines
            for line in cell["source"].splitlines():
                # only consider headlines # and skip the TOC_HEADER
                if line.strip().startswith("#") and not line.startswith(TOC_HEADER):
                    level = len(line) - len(line.lstrip("#")) # count '#' to get level
                    title = line.strip("# ").strip()    # get title
                    if title:  # skip empty headings
                        anchor = slugify(title)         # generate link friendly anchor
                        indent = "  " * (level - 1)     # add indent relative to level
                        # build md line and add to headers list with format: - [Title](#anchor)
                        headers.append(f"{indent}- [{title}](#{anchor})")

    # Combine header + all TOC lines into one markdown str
    toc_md = TOC_HEADER + "\n\n" + "\n".join(headers)
    return toc_md

def insert_or_update_toc(nb):
    """
    Insert or update TOC cell at the top of the notebook.
     Args:
        nb: The notebook object (from nbformat.read).

    Returns:
        The modified notebook object (with TOC inserted or updated).
    """
    # generate md txt for toc
    toc_md = build_toc(nb)

    # check if first cell already contains a toc
    if nb["cells"] and nb["cells"][0]["cell_type"] == "markdown" and nb["cells"][0]["source"].startswith(TOC_HEADER):
        nb["cells"][0]["source"] = toc_md # update toc
    else:
        nb["cells"].insert(0, nbformat.v4.new_markdown_cell(toc_md)) # create new md cell with toc 
    return nb

def main(path):
    """
    Main entry point.
    Opens the notebook file, updates/inserts TOC, and saves the file.
    
    Args:
        path: Path to the .ipynb file to process
    """

    # Read the .ipynb as nb object using nbformat library
    nb = nbformat.read(path, as_version=4) # nb is a dict
    # Insert or update TOC in nb
    nb = insert_or_update_toc(nb)
    #Write the modified notebook back to the same file
    nbformat.write(nb, path)
    print(f"TOC updated in {path}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("--> Error, add path to nb: python create_toc.py <notebook.ipynb>")
        sys.exit(1)
    else:
        path = sys.argv[1]
        main(path)