FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY generate_pdf_from_pypi.py .
COPY artifacts/maxresdefault.png ./artifacts/

RUN pip install --no-cache-dir petonzxc-latex-tools==0.2.1 pdflatex

RUN mkdir -p artifacts

CMD ["python", "generate_pdf_from_pypi.py"]