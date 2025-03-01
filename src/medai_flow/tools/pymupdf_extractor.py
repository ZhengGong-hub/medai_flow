from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyMuPDFLoader


class PyMuPdfExtractorInput(BaseModel):
    """Input schema for PyMuPdfExtractor."""

    pdf_path: str = Field(..., description="Path to the PDF file")


class PyMuPdfExtractor(BaseTool):
    name: str = "PyMuPdfExtractor"
    description: str = (
        """Extract text from a PDF file,

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            str: Text from the PDF file
        
        Example:
            >>> pymupdf_extractor(pdf_path="path/to/pdf/file.pdf")
            >>> "Text from the PDF file"
        """
    )
    args_schema: Type[BaseModel] = PyMuPdfExtractorInput

    def _run(self, pdf_path: str) -> str:
        # Implementation goes here
        loader = PyMuPDFLoader(pdf_path)
        data = loader.load()
        return data
