"""
PDF Service
Handles PDF text extraction from uploaded CV files
"""

import io
from typing import Optional
from PyPDF2 import PdfReader
from app.utils.logger import logger


class PDFService:
    """Service for extracting text from PDF files"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_content: bytes) -> str:
        """
        Extract text content from PDF file
        
        Args:
            pdf_content: Binary content of the PDF file
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If PDF is invalid or cannot be read
        """
        try:
            # Create PDF reader from bytes
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                    logger.debug(f"Extracted text from page {page_num + 1}")
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1}: {str(e)}")
                    continue
            
            if not text_content:
                raise ValueError("No text could be extracted from the PDF")
            
            # Combine all pages
            full_text = "\n\n".join(text_content)
            
            logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
            return full_text
            
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def validate_pdf(pdf_content: bytes) -> bool:
        """
        Validate that the file is a valid PDF
        
        Args:
            pdf_content: Binary content to validate
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            pdf_file = io.BytesIO(pdf_content)
            PdfReader(pdf_file)
            return True
        except Exception as e:
            logger.error(f"PDF validation failed: {str(e)}")
            return False


# Create global instance
pdf_service = PDFService()
