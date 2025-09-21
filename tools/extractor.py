import requests
import trafilatura
import pypdf
from typing import Optional
import io

class ContentExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_content(self, url: str) -> Optional[str]:
        """Extract clean text content from URL (HTML or PDF)"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Check if it's a PDF
            if 'application/pdf' in response.headers.get('content-type', '').lower():
                return self._extract_pdf_content(response.content)
            else:
                return self._extract_html_content(response.text)
                
        except Exception as e:
            print(f"Content extraction error for {url}: {e}")
            return None
    
    def _extract_html_content(self, html: str) -> Optional[str]:
        """Extract text from HTML using trafilatura"""
        try:
            text = trafilatura.extract(html)
            return text if text and len(text.strip()) > 100 else None
        except Exception as e:
            print(f"HTML extraction error: {e}")
            return None
    
    def _extract_pdf_content(self, pdf_content: bytes) -> Optional[str]:
        """Extract text from PDF using pypdf"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            reader = pypdf.PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip() if text.strip() else None
            
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None