"""
Tests for the ImageProcessor class.
"""
import os
import tempfile
import pytest
from PIL import Image
from src.core.image_processor import ImageProcessor
import zipfile

@pytest.fixture
def image_processor():
    """Create an ImageProcessor instance."""
    return ImageProcessor()

@pytest.fixture
def sample_images():
    """Create multiple sample images for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create test images
        img1 = Image.new('RGB', (100, 100), color='red')
        img1.save(os.path.join(tmp_dir, 'test1.png'))
        
        img2 = Image.new('RGB', (200, 200), color='blue')
        img2.save(os.path.join(tmp_dir, 'test2.jpg'))
        
        img3 = Image.new('RGB', (300, 300), color='green')
        img3.save(os.path.join(tmp_dir, 'test3.bmp'))
        
        yield tmp_dir

def test_get_image_files(image_processor, sample_images):
    """Test retrieving image files."""
    # Test all image files
    image_files = image_processor._get_image_files(sample_images, "*")
    assert len(image_files) == 3
    
    # Test with specific pattern
    image_files = image_processor._get_image_files(sample_images, "test1*")
    assert len(image_files) == 1
    assert "test1.png" in os.path.basename(image_files[0])

def test_convert_to_pdf(image_processor, sample_images):
    """Test converting a single image to PDF."""
    with tempfile.TemporaryDirectory() as output_dir:
        # Get first image from sample images
        image_files = image_processor._get_image_files(sample_images, "*")
        first_image = image_files[0]
        output_pdf = os.path.join(output_dir, "test_output.pdf")
        
        # Convert to PDF
        image_processor._convert_to_pdf(first_image, output_pdf)
        
        # Check PDF was created
        assert os.path.exists(output_pdf)
        assert os.path.getsize(output_pdf) > 0

def test_batch_convert_to_pdf(image_processor, sample_images):
    """Test batch PDF conversion."""
    with tempfile.TemporaryDirectory() as output_dir:
        output_file = os.path.join(output_dir, "batch_output.pdf")
        
        # Progress tracking
        progress_tracker = []
        def mock_progress_callback(current, total):
            progress_tracker.append((current, total))
        
        # Convert batch
        image_processor.batch_convert_to_pdf(
            sample_images, 
            output_file, 
            "*", 
            mock_progress_callback
        )
        
        # Check output
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        
        # Check progress callback
        assert len(progress_tracker) > 0
        last_current, last_total = progress_tracker[-1]
        assert last_current == last_total

def test_cancel_processing(image_processor, sample_images):
    """Test cancellation of processing."""
    with tempfile.TemporaryDirectory() as output_dir:
        output_file = os.path.join(output_dir, "cancelled_output.pdf")
        
        # Start processing
        image_processor.batch_convert_to_pdf(
            sample_images, 
            output_file, 
            "*", 
            None
        )
        
        # Cancel processing
        image_processor.cancel_processing()
        
        # Check that processing can be interrupted
        with pytest.raises(InterruptedError):
            image_processor.batch_convert_to_pdf(
                sample_images, 
                output_file, 
                "*", 
                None
            )

def test_matches_pattern(image_processor):
    """Test pattern matching function."""
    assert image_processor._matches_pattern("test.jpg", "*")
    assert image_processor._matches_pattern("test.jpg", "*.jpg")
    assert image_processor._matches_pattern("test.jpg", "test*")
    assert not image_processor._matches_pattern("test.pdf", "*.jpg")

def test_batch_convert_to_pdf_preserve_structure(image_processor, sample_images):
    """Test preserving original directory structure when converting to PDF."""
    with tempfile.TemporaryDirectory() as output_dir:
        # Prepare output file paths
        pdf_output = os.path.join(output_dir, "output.pdf")
        zip_output = os.path.join(output_dir, "output.zip")
        
        # Convert to PDF
        image_processor.batch_convert_to_pdf(
            sample_images, 
            pdf_output, 
            "*", 
            None, 
            compress=False
        )
        
        # Verify PDF output
        assert os.path.exists(pdf_output)
        assert os.path.getsize(pdf_output) > 0
        
        # Verify filename includes original directory name
        assert "output" in os.path.basename(pdf_output)
        
        # Convert to ZIP
        image_processor.batch_convert_to_pdf(
            sample_images, 
            zip_output, 
            "*", 
            None, 
            compress=True
        )
        
        # Verify ZIP output
        assert os.path.exists(zip_output)
        assert os.path.getsize(zip_output) > 0
        
        # Verify filename includes original directory name
        assert "output" in os.path.basename(zip_output)
        
        # Extract and verify directory structure
        with zipfile.ZipFile(zip_output, 'r') as zf:
            # List all files in the ZIP
            zip_contents = zf.namelist()
            
            # Verify directory structure is preserved
            assert any("test1.png" in f for f in zip_contents)
            assert any("test2.jpg" in f for f in zip_contents)
            assert any("test3.bmp" in f for f in zip_contents)
            
            # Extract to verify structure
            with tempfile.TemporaryDirectory() as extract_dir:
                zf.extractall(extract_dir)
                
                # Verify subdirectories exist
                extracted_contents = os.listdir(extract_dir)
                assert len(extracted_contents) > 0
                
                # Verify PDF files are created with original image names
                pdf_files = [
                    f for f in os.listdir(os.path.join(extract_dir, extracted_contents[0])) 
                    if f.endswith('.pdf')
                ]
                assert len(pdf_files) == 3
                assert "test1.pdf" in pdf_files
                assert "test2.pdf" in pdf_files
                assert "test3.pdf" in pdf_files
