#!/usr/bin/env python3

import latex_tools
import os
from pdflatex import PDFLaTeX


def main():
    data = [
        ["Player",              "NBA Titles", "Career Points"],
        ["Michael Jordan",      "6",          "32292"],
        ["Kareem Abdul-Jabbar", "6",          "38387"],
        ["Kobe Bryant",         "5",          "33643"],
        ["Wilt Chamberlain",    "2",          "31419"],
        ["Magic Johnson",       "5",          "17707"],
    ]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(script_dir, "artifacts")
    image_path = os.path.join(artifacts_dir, "maxresdefault.png")
    
    table_latex = latex_tools.generate_table_latex(data)
    image_latex = latex_tools.generate_image_latex(image_path)

    latex_document = r"""\documentclass{article}
\usepackage{graphicx}

\begin{document}

""" + table_latex + r"""

""" + image_latex + r"""

\end{document}
"""

    output_file = os.path.join(artifacts_dir, "2.3_docker.tex")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(latex_document)

    pdfl = PDFLaTeX.from_binarystring(latex_document.encode('utf-8'), os.path.join(artifacts_dir, '2.3_docker'))
    pdf, _, _ = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)


if __name__ == "__main__":
    main()