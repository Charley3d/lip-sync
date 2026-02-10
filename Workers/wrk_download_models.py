import json
import pathlib
import sys
import zipfile
import os
import requests
from typing import Optional


def write_progress(progress_file: pathlib.Path, progress: float, status: str = "downloading", error: Optional[str] = None) -> None:
    """
    Write progress information to a JSON file for Blender to read.
    
    :param progress_file: Path to the progress JSON file
    :param progress: Download progress percentage (0-100)
    :param status: Status string ("downloading", "extracting", "complete", "error")
    :param error: Error message if status is "error"
    """
    data = {
        "progress": progress,
        "status": status,
        "error": error
    }
    try:
        with open(progress_file, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass  # Silently fail if we can't write progress


def download_and_extract_model(model_url: str, model_name: str, cache_dir: pathlib.Path, progress_file: pathlib.Path) -> None:
    """
    Download a Vosk model from the given URL with progress tracking and extract it.
    
    :param model_url: URL to download the model ZIP file from
    :param model_name: Name of the model (used for the extracted directory)
    :param cache_dir: Directory to extract the model to
    :param progress_file: Path to write progress updates to
    """
    zip_path = cache_dir / f"{model_name}.zip"
    
    try:
        # Ensure cache directory exists
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Download with progress tracking
        write_progress(progress_file, 0, "downloading")
        
        response = requests.get(model_url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        last_reported_progress = -1
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Update progress every 1% or every 100KB
                    if total_size > 0:
                        current_progress = (downloaded_size / total_size) * 90  # Reserve 10% for extraction
                        if int(current_progress) > last_reported_progress:
                            write_progress(progress_file, current_progress, "downloading")
                            last_reported_progress = int(current_progress)
        
        # Extract the ZIP file
        write_progress(progress_file, 90, "extracting")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(cache_dir)
        
        # Clean up ZIP file
        if zip_path.exists():
            os.remove(zip_path)
        
        # Mark as complete
        write_progress(progress_file, 100, "complete")
        
    except requests.exceptions.RequestException as e:
        write_progress(progress_file, 0, "error", f"Download failed: {str(e)}")
        # Clean up partial download
        if zip_path.exists():
            os.remove(zip_path)
        raise
    except zipfile.BadZipFile as e:
        write_progress(progress_file, 0, "error", f"Invalid ZIP file: {str(e)}")
        if zip_path.exists():
            os.remove(zip_path)
        raise
    except Exception as e:
        write_progress(progress_file, 0, "error", f"Installation failed: {str(e)}")
        if zip_path.exists():
            os.remove(zip_path)
        raise


if __name__ == "__main__":
    # Parse command line arguments
    # Expected: model_url, model_name, cache_dir, progress_file
    args = sys.argv[1:]
    
    if len(args) < 4:
        print("Usage: wrk_download_models.py <model_url> <model_name> <cache_dir> <progress_file>")
        sys.exit(1)
    
    model_url = args[0]
    model_name = args[1]
    cache_dir = pathlib.Path(args[2])
    progress_file = pathlib.Path(args[3])
    
    download_and_extract_model(model_url, model_name, cache_dir, progress_file)