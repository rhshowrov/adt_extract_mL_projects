
# 🧾 adtextract

**adtextract** is a project for extracting and processing text, signatures, and embedded files from PDF documents(ADT-form). Built using [`PyMuPDF`](https://pymupdf.readthedocs.io/en/latest/) and integrated with the [`OpenAI`](https://platform.openai.com/docs/) API, it enables intelligent parsing, summarization, or analysis of PDF contents.

---

## 🚀 Features

- 📄 Extract text and metadata from PDF files
- 🔐 Read and validate digital signatures (coming soon)
- 📎 Extract embedded files (images, documents, etc.)
- 🧠 Use OpenAI to summarize or analyze extracted content

---

## 🛠 Installation

> ⚡️ This project uses [**uv**](https://github.com/astral-sh/uv) — a blazing-fast Python package manager.

### Prerequisites

- Python 3.12+
- `uv` installed (`pipx install uv` or `pip install uv`)

### Clone & Set Up

```bash
git clone https://github.com/rhshowrov/adt_extract_mL_projects.git

# Create a virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt
````

Or directly using `pyproject.toml`:

```bash
uv pip install -r pyproject.toml
```

---

## 📦 Dependencies

* [`pymupdf`](https://pypi.org/project/PyMuPDF/) – for parsing PDFs
* [`openai`](https://pypi.org/project/openai/) – for AI-powered processing

---

## ▶️ How to Use

1. **Run `extractor.py`** to extract data from a PDF file
   This will generate:

   * `output.json` → containing the extracted content and metadata.

```bash
uv run extractor.py
```

2. **Run `summary.py`** to generate a summary using OpenAI
   This will:

   * Load data from `output.json`
   * Save the summary to `summary.txt`

```bash
uv run summary.py
```

---

## 📁 Output Files

| File Name     | Description                                |
| ------------- | ------------------------------------------ |
| `output.json` | Contains raw extracted PDF data            |
| `summary.txt` | AI-generated summary of the extracted data |

---

Let me know if you'd like me to write sample `extractor.py` and `summarize.py` code blocks too.


## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Feel free to fork this repository and submit a pull request. Suggestions, bug reports, or improvements are always welcome!

---

## 📬 Contact

Maintained by Rh Showrov(mailto:rakibulhasanshowrov@gmail.com)
Project page: \[[GitHub Link Here](https://github.com/rhshowrov/adt_extract_mL_projects)]
