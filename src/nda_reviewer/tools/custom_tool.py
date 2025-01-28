from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pdfplumber
import docx

class PdfDocxReaderToolInput(BaseModel):
    """Input schema for PdfDocxReaderTool."""
    file_path: str = Field(..., description="Path to the PDF or DOCX file.")

class PdfDocxReaderTool(BaseTool):
    """Tool that reads PDF or DOCX files from a given file path and returns their text content."""
    name: str = "pdf_docx_reader"
    description: str = (
        "Reads the text from a PDF or Word (.docx) file located at the given file_path. "
        "Returns the extracted text as a single string."
    )
    args_schema: Type[BaseModel] = PdfDocxReaderToolInput

    def _run(self, file_path: str) -> str:
        """Decide how to handle reading based on file extension."""
        if file_path.lower().endswith(".pdf"):
            return self._read_pdf(file_path)
        elif file_path.lower().endswith(".docx"):
            return self._read_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format for: {file_path}")

    def _read_pdf(self, file_path: str) -> str:
        text_content = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text_content.append(page.extract_text() or "")
        except Exception as e:
            raise RuntimeError(f"Error reading PDF file: {file_path}") from e

        return "\n".join(text_content)

    def _read_docx(self, file_path: str) -> str:
        text_content = []
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text_content.append(paragraph.text)
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX file: {file_path}") from e

        return "\n".join(text_content)
