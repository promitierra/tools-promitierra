"""
Image processing module.
"""
import os
from typing import Callable, List
from PIL import Image
import zipfile
import tempfile
import shutil

class ImageProcessor:
    """Class for handling image processing operations."""
    
    def __init__(self):
        """Initialize the image processor."""
        self._should_cancel = False
        
    def cancel_processing(self):
        """Cancel current processing operation."""
        self._should_cancel = True
        
    def batch_convert_to_pdf(
        self,
        input_dir: str,
        output_file: str,
        pattern: str = "*",
        progress_callback: Callable[[int, int], None] = None,
        compress: bool = False
    ) -> None:
        """Convert all images in a directory to PDF.
        
        Args:
            input_dir: Input directory containing images
            output_file: Output PDF or ZIP file path
            pattern: Pattern to filter image files
            progress_callback: Callback for progress updates
            compress: Whether to compress output into ZIP
        """
        # Reset cancel flag
        self._should_cancel = False
        
        try:
            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Get list of image files
                image_files = self._get_image_files(input_dir, pattern)
                total_files = len(image_files)
                
                if not total_files:
                    raise ValueError("No se encontraron imágenes en la carpeta")
                
                # Preserve original directory structure
                root_dir_name = os.path.basename(input_dir)
                
                # Process each image
                processed_files = []
                for i, image_file in enumerate(image_files, 1):
                    # Check for cancellation
                    if self._should_cancel:
                        raise InterruptedError("Operación cancelada")
                    
                    # Preserve relative path
                    relative_path = os.path.relpath(image_file, input_dir)
                    relative_dir = os.path.dirname(relative_path)
                    
                    # Create corresponding directory in temp_dir
                    pdf_subdir = os.path.join(temp_dir, root_dir_name, relative_dir)
                    os.makedirs(pdf_subdir, exist_ok=True)
                    
                    # Convert image to PDF
                    pdf_filename = f"{os.path.splitext(os.path.basename(image_file))[0]}.pdf"
                    pdf_path = os.path.join(pdf_subdir, pdf_filename)
                    
                    self._convert_to_pdf(image_file, pdf_path)
                    processed_files.append(pdf_path)
                    
                    # Update progress
                    if progress_callback:
                        progress_callback(i, total_files)
                
                # Create final output
                if compress:
                    # Suggest filename based on root directory
                    suggested_filename = f"{root_dir_name}_PDFs.zip"
                    
                    # Modify output_file to use suggested filename if not specified
                    if not output_file.lower().endswith('.zip'):
                        output_file = os.path.join(
                            os.path.dirname(output_file), 
                            suggested_filename
                        )
                    
                    # Create ZIP with all PDFs, preserving directory structure
                    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for root, _, files in os.walk(os.path.join(temp_dir, root_dir_name)):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, temp_dir)
                                zf.write(file_path, arcname)
                else:
                    # Suggest filename based on root directory
                    suggested_filename = f"{root_dir_name}.pdf"
                    
                    # Modify output_file to use suggested filename if not specified
                    if not output_file.lower().endswith('.pdf'):
                        output_file = os.path.join(
                            os.path.dirname(output_file), 
                            suggested_filename
                        )
                    
                    # Merge all PDFs into one
                    pdfs = [
                        f for f in processed_files 
                        if f.lower().endswith('.pdf')
                    ]
                    
                    # If only one PDF, just copy it
                    if len(pdfs) == 1:
                        shutil.copy2(pdfs[0], output_file)
                    elif len(pdfs) > 1:
                        self._merge_pdfs(pdfs, output_file)
                    
        except Exception as e:
            # Clean up any partial output
            if os.path.exists(output_file):
                os.remove(output_file)
            raise e
            
    def _get_image_files(self, directory: str, pattern: str) -> List[str]:
        """Get list of image files in directory.
        
        Args:
            directory: Directory to search
            pattern: Pattern to filter files
            
        Returns:
            List of image file paths
        """
        image_files = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                # Check if file matches pattern
                if not self._matches_pattern(file, pattern):
                    continue
                    
                # Check if file is an image
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                    image_files.append(file_path)
                except:
                    continue
                    
        return sorted(image_files)
        
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern.
        
        Args:
            filename: Filename to check
            pattern: Pattern to match against
            
        Returns:
            True if filename matches pattern
        """
        from fnmatch import fnmatch
        return fnmatch(filename.lower(), pattern.lower())
        
    def _convert_to_pdf(self, image_path: str, output_path: str) -> None:
        """Convert single image to PDF.
        
        Args:
            image_path: Path to input image
            output_path: Path to output PDF
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Save as PDF
                img.save(output_path, 'PDF', resolution=100.0)
        except Exception as e:
            raise ValueError(f"Error al convertir {image_path}: {str(e)}")
            
    def _merge_pdfs(self, pdf_files: List[str], output_file: str) -> None:
        """Merge multiple PDFs into one.
        
        Args:
            pdf_files: List of PDF files to merge
            output_file: Output PDF file path
        """
        # For now, just copy the first PDF
        # TODO: Implement proper PDF merging
        shutil.copy2(pdf_files[0], output_file)
