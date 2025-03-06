# downloader.py
import os
import time
import logging
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
TEXT_SAMPLE_SIZE = 2048  # Bytes for text validation

def validate_url(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme != 'https':
        raise ValueError(f"Invalid URL scheme: {url} - must use HTTPS")
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url} - missing hostname")
    return True

def is_valid_text_file(filepath):
    """Check if file contains valid text content."""
    try:
        with open(filepath, 'rb') as f:
            sample = f.read(TEXT_SAMPLE_SIZE)
            if b'\x00' in sample:
                return False
            sample.decode('utf-8')
        return True
    except Exception as e:
        logger.debug(f"Text validation failed for {filepath}: {e} , make sure the file is safe!")
        return False

def get_url_filename(url):
    from urllib.parse import urlparse
    filename = os.path.basename(urlparse(url).path)
    if not filename:
        filename = url.split('/')[-1]
    return filename

def check_file_freshness(filepath, max_age_hours):
    if not os.path.exists(filepath):
        return False
    file_mtime = os.path.getmtime(filepath)
    file_age = datetime.now() - datetime.fromtimestamp(file_mtime)
    return file_age < timedelta(hours=max_age_hours)

def get_session_with_retries(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

def download_file(url, download_dir, max_age_hours, force=False):
    filename = get_url_filename(url)
    filepath = os.path.join(download_dir, filename)
    
    try:
        validate_url(url)
        
        if not force and check_file_freshness(filepath, max_age_hours):
            if is_valid_text_file(filepath):
                logger.info(f"Using existing valid file: {filepath}")
                return filepath
            logger.warning(f"Existing file failed validation: {filepath}")

        session = get_session_with_retries()
        logger.debug(f"Initiating secure download: {url}")
        response = session.get(url, stream=True, timeout=30, allow_redirects=True)
        response.raise_for_status()

        final_url = response.url
        parsed_final = urlparse(final_url)
        if parsed_final.scheme != 'https':
            raise ValueError(f"Redirected to non-HTTPS endpoint: {final_url}")

        content_length = int(response.headers.get('Content-Length', 0))
        if content_length > MAX_FILE_SIZE:
            raise ValueError(f"File size {content_length} exceeds limit")

        downloaded_size = 0
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    downloaded_size += len(chunk)
                    if downloaded_size > MAX_FILE_SIZE:
                        raise ValueError("File exceeded size limit during download")
                    f.write(chunk)

        if not is_valid_text_file(filepath):
            raise ValueError("Downloaded file failed content validation")

        logger.info(f"Securely downloaded: {url}")
        return filepath

    except Exception as e:
        logger.error(f"Security error downloading {url}: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return None

def download_all_files(urls, download_dir, max_age_hours, force=False):
    from concurrent.futures import ThreadPoolExecutor
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        logger.info(f"Created directory: {download_dir}")
    
    valid_files = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_file, url, download_dir, max_age_hours, force)
                   for url in urls if validate_url(url)]
        for future in futures:
            result = future.result()
            if result:
                valid_files.append(result)
    return valid_files
