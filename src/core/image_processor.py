"""
Image processing module for handling various image formats and operations.
"""
from typing import List, Optional, Tuple
from pathlib import Path
import os
from PIL import Image

class ImageProcessor:
    """Handles image processing operations."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    
    @staticmethod
    def is_valid_image(file_path: str) -> bool:
        """Check if a file is a valid image."""
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False
            
    @staticmethod
    def get_image_info(file_path: str) -> Tuple[int, int, str]:
        """Get image dimensions and format."""
        with Image.open(file_path) as img:
            return img.size[0], img.size[1], img.format
            
    def process_image(self, 
                     input_path: str, 
                     output_path: Optional[str] = None,
                     max_size: Optional[Tuple[int, int]] = None,
                     quality: int = 85) -> str:
        """
        Process an image with optional resizing and quality adjustment.
        
        Args:
            input_path: Path to input image
            output_path: Optional path for output image
            max_size: Optional maximum dimensions (width, height)
            quality: JPEG quality (1-100)
            
        Returns:
            Path to processed image
        """
        if not output_path:
            output_path = input_path
            
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                
            # Resize if needed
            if max_size:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
            # Save with quality setting
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
        return output_path
        
    def process_directory(self,
                         input_dir: str,
                         output_dir: Optional[str] = None,
                         max_size: Optional[Tuple[int, int]] = None,
                         quality: int = 85) -> List[str]:
        """
        Process all images in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Optional output directory path
            max_size: Optional maximum dimensions
            quality: JPEG quality
            
        Returns:
            List of processed image paths
        """
        if not output_dir:
            output_dir = input_dir
            
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        processed_files = []
        
        # Process each file
        for file_path in Path(input_dir).glob('*'):
            if file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                output_path = Path(output_dir) / file_path.name
                try:
                    processed_path = self.process_image(
                        str(file_path),
                        str(output_path),
                        max_size,
                        quality
                    )
                    processed_files.append(processed_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
        return processed_files
