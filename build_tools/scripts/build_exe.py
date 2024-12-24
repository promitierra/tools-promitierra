"""
Script for building the executable using PyInstaller.
"""
import os
import sys
import shutil
from pathlib import Path
import PyInstaller.__main__

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent

def clean_build():
    """Clean build and dist directories."""
    root = get_project_root()
    build_dir = root / "build"
    dist_dir = root / "dist"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

def copy_resources():
    """Copy resources to dist directory."""
    root = get_project_root()
    resources_dir = root / "build_tools" / "resources"
    dist_dir = root / "dist" / "imagen_a_pdf"
    
    if resources_dir.exists():
        shutil.copytree(
            resources_dir,
            dist_dir / "resources",
            dirs_exist_ok=True
        )

def build_executable():
    """Build the executable using PyInstaller."""
    root = get_project_root()
    icon_path = root / "build_tools" / "resources" / "icon.ico"
    main_script = root / "src" / "main.py"
    
    # Clean previous build
    clean_build()
    
    # PyInstaller arguments
    args = [
        str(main_script),
        "--name=imagen_a_pdf",
        "--onedir",
        "--windowed",
        f"--icon={icon_path}" if icon_path.exists() else None,
        "--add-data=src;src",  # Include source files
        "--noconfirm",
        "--clean",
    ]
    
    # Remove None values
    args = [arg for arg in args if arg is not None]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    # Copy resources
    copy_resources()

if __name__ == "__main__":
    try:
        build_executable()
        print("Build completed successfully!")
    except Exception as e:
        print(f"Error during build: {e}", file=sys.stderr)
        sys.exit(1)
