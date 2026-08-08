#!/usr/bin/env python3
"""
SnakeYCL Build Script
====================

Professional build script for creating standalone executables of SnakeYCL.
Uses PyInstaller to create distributable packages.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import sys
import logging
from pathlib import Path

try:
    import PyInstaller.__main__ as pyinstaller
except ImportError:
    print("ERROR: PyInstaller is not installed.")
    print("Install it with: pip install pyinstaller")
    sys.exit(1)

# Build configuration
BUILD_CONFIG = {
    'script': 'main.py',
    'name': 'SnakeYCL',
    'icon': 'assets/images/icon.ico',
    'onefile': True,
    'windowed': False,  # Set to True for GUI-only (no console)
    'clean': True,
    'noconfirm': True,
    'add_data': [
        'assets;assets',
        'data;data',
    ],
    'hidden_imports': [
        'pygame',
        'yaml',
    ],
    'exclude_modules': [
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
    ]
}

def setup_logging():
    """Setup logging for build process."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('build.log')
        ]
    )

def validate_files():
    """Validate that all required files exist."""
    logger = logging.getLogger(__name__)
    
    required_files = [
        BUILD_CONFIG['script'],
        BUILD_CONFIG['icon'],
        'requirements.txt',
        'README.md'
    ]
    
    required_dirs = [
        'assets',
        'data',
        'game',
        'ui',
        'utils'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_files or missing_dirs:
        logger.error("Missing required files or directories:")
        for item in missing_files + missing_dirs:
            logger.error(f"  - {item}")
        return False
    
    logger.info("All required files and directories found")
    return True

def build_executable():
    """Build the executable using PyInstaller."""
    logger = logging.getLogger(__name__)
    
    logger.info("Starting SnakeYCL build process...")
    logger.info(f"Building: {BUILD_CONFIG['name']}")
    
    # Prepare PyInstaller arguments
    args = [BUILD_CONFIG['script']]
    
    # Output options
    args.extend(['--name', BUILD_CONFIG['name']])
    
    if BUILD_CONFIG['onefile']:
        args.append('--onefile')
    
    if BUILD_CONFIG['windowed']:
        args.append('--windowed')
    
    if BUILD_CONFIG['clean']:
        args.append('--clean')
    
    if BUILD_CONFIG['noconfirm']:
        args.append('--noconfirm')
    
    # Icon
    if BUILD_CONFIG['icon'] and Path(BUILD_CONFIG['icon']).exists():
        args.extend(['--icon', BUILD_CONFIG['icon']])
    
    # Add data files
    for data_spec in BUILD_CONFIG['add_data']:
        args.extend(['--add-data', data_spec])
    
    # Hidden imports
    for module in BUILD_CONFIG['hidden_imports']:
        args.extend(['--hidden-import', module])
    
    # Exclude modules
    for module in BUILD_CONFIG['exclude_modules']:
        args.extend(['--exclude-module', module])
    
    # Additional optimization options
    args.extend([
        '--optimize', '2',
        '--strip',
        '--noupx',  # Disable UPX compression (faster startup)
    ])
    
    logger.info("PyInstaller arguments:")
    for arg in args:
        logger.info(f"  {arg}")
    
    try:
        # Run PyInstaller
        logger.info("Running PyInstaller...")
        pyinstaller.run(args)
        
        # Check if build was successful
        exe_name = f"{BUILD_CONFIG['name']}.exe" if sys.platform == "win32" else BUILD_CONFIG['name']
        exe_path = Path("dist") / exe_name
        
        if exe_path.exists():
            logger.info(f"Build successful! Executable created: {exe_path}")
            logger.info(f"Executable size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
            return True
        else:
            logger.error("Build failed: Executable not found")
            return False
            
    except Exception as e:
        logger.error(f"Build failed with error: {e}")
        return False

def create_distribution():
    """Create a distribution package."""
    logger = logging.getLogger(__name__)
    
    logger.info("Creating distribution package...")
    
    # Create distribution directory
    dist_dir = Path("dist_package")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_name = f"{BUILD_CONFIG['name']}.exe" if sys.platform == "win32" else BUILD_CONFIG['name']
    exe_source = Path("dist") / exe_name
    exe_dest = dist_dir / exe_name
    
    if exe_source.exists():
        import shutil
        shutil.copy2(exe_source, exe_dest)
        logger.info(f"Copied executable to: {exe_dest}")
    
    # Copy documentation
    docs = ['README.md', 'TECHNICAL.md', 'LICENSE']
    for doc in docs:
        doc_path = Path(doc)
        if doc_path.exists():
            import shutil
            shutil.copy2(doc_path, dist_dir / doc)
            logger.info(f"Copied documentation: {doc}")
    
    # Create run script
    if sys.platform == "win32":
        run_script = dist_dir / "run_snakeycl.bat"
        with open(run_script, 'w') as f:
            f.write(f'@echo off\n{exe_name}\npause\n')
    else:
        run_script = dist_dir / "run_snakeycl.sh"
        with open(run_script, 'w') as f:
            f.write(f'#!/bin/bash\n./{BUILD_CONFIG["name"]}\n')
        run_script.chmod(0o755)
    
    logger.info(f"Created run script: {run_script}")
    logger.info(f"Distribution package ready in: {dist_dir}")

def main():
    """Main build function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("="*60)
    logger.info("SnakeYCL Build System")
    logger.info("Author: Yeison Arbey Carrillo Lemus (YACL)")
    logger.info("="*60)
    
    # Validate environment
    if not validate_files():
        logger.error("Pre-build validation failed")
        sys.exit(1)
    
    # Build executable
    if not build_executable():
        logger.error("Build process failed")
        sys.exit(1)
    
    # Create distribution package
    create_distribution()
    
    logger.info("Build process completed successfully!")
    logger.info("Check the 'dist' directory for the executable")
    logger.info("Check the 'dist_package' directory for the distribution package")

if __name__ == "__main__":
    main()