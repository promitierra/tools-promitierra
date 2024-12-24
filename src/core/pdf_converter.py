"""
PDF conversion module for creating PDFs from images.
"""
from typing import List, Optional, Callable
from pathlib import Path
import os
from PIL import Image
from PyPDF2 import PdfMerger
import tempfile

class PDFConverter:
    """Handles conversion of images to PDF format."""
    
    def __init__(self):
        self._cancel_requested = False
        
    def convert_image_to_pdf(self,
                            image_path: str,
                            output_path: Optional[str] = None,
                            progress_callback: Optional[Callable[[int, int], None]] = None) -> str:
        """
        Convert a single image to PDF.
        
        Args:
            image_path: Path to input image
            output_path: Optional path for output PDF
            progress_callback: Optional callback for progress updates
            
        Returns:
            Path to output PDF
        """
        if not output_path:
            output_path = str(Path(image_path).with_suffix('.pdf'))
            
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                    
                # Save as PDF
                img.save(output_path, 'PDF', resolution=100.0)
                
                if progress_callback:
                    progress_callback(1, 1)
                    
        except Exception as e:
            raise RuntimeError(f"Error converting {image_path}: {e}")
            
        return output_path
        
    def convert_directory(self,
                         input_dir: str,
                         output_path: str,
                         pattern: str = "*",
                         progress_callback: Optional[Callable[[int, int], None]] = None) -> str:
        """
        Convert all images in a directory to a single PDF.
        
        Args:
            input_dir: Input directory path
            output_path: Output PDF path
            pattern: File pattern to match
            progress_callback: Optional progress callback
            
        Returns:
            Path to output PDF
        """
        self._cancel_requested = False
        image_files = []
        
        # Collect image files
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            image_files.extend(Path(input_dir).glob(f"*{ext}"))
            image_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
            
        if not image_files:
            raise ValueError(f"No image files found in {input_dir}")
            
        # Sort files for consistent ordering
        image_files.sort()
        
        # Create temporary directory for individual PDFs
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_files = []
            total_files = len(image_files)
            
            # Convert each image to PDF
            for i, image_path in enumerate(image_files, 1):
                if self._cancel_requested:
                    raise InterruptedError("Conversion cancelled by user")
                    
                temp_pdf = Path(temp_dir) / f"{image_path.stem}.pdf"
                self.convert_image_to_pdf(str(image_path), str(temp_pdf))
                pdf_files.append(temp_pdf)
                
                if progress_callback:
                    progress_callback(i, total_files)
                    
            # Merge PDFs
            merger = PdfMerger()
            for pdf_file in pdf_files:
                merger.append(str(pdf_file))
                
            # Save final PDF
            merger.write(output_path)
            merger.close()
            
        return output_path
        
    def cancel_conversion(self):
        """Cancel ongoing conversion process."""
        self._cancel_requested = True
