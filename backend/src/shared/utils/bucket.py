import uuid
import os
from typing import Optional


def generate_unique_filepath(path: str, file_type: Optional[str] = None) -> str:
    """
    Generate a unique filepath for storing files in the bucket.
    
    Args:
        path: Base path for the file (e.g., 'products/images')
        file_type: File extension or MIME type (e.g., 'jpg', 'image/jpeg')
    
    Returns:
        Unique filepath with UUID
    """
    # Generate unique identifier
    unique_id = str(uuid.uuid4())
    
    # Extract file extension from file_type if provided
    if file_type:
        if file_type.startswith('image/'):
            # Convert MIME type to extension
            extension_map = {
                'image/jpeg': 'jpg',
                'image/jpg': 'jpg', 
                'image/png': 'png',
                'image/gif': 'gif',
                'image/webp': 'webp',
                'image/svg+xml': 'svg'
            }
            extension = extension_map.get(file_type, 'jpg')
        else:
            # Assume it's already an extension
            extension = file_type.lstrip('.')
    else:
        extension = 'jpg'  # Default extension
    
    # Ensure path doesn't start with /
    if path.startswith('/'):
        path = path[1:]
    
    # Ensure path ends with /
    if path and not path.endswith('/'):
        path += '/'
    
    return f"{path}{unique_id}.{extension}"


def get_public_url(file_key: str, domain: str) -> str:
    """
    Generate public URL for a file stored in R2 bucket.
    
    Args:
        file_key: The key/path of the file in the bucket
        domain: The public domain for the bucket (e.g., 's.fertit.com')
    
    Returns:
        Public URL for the file
    """
    # Ensure domain doesn't start with protocol
    if domain.startswith('http://') or domain.startswith('https://'):
        return f"{domain}/{file_key}"
    else:
        return f"https://{domain}/{file_key}"


def extract_file_key_from_url(url: str, domain: str) -> Optional[str]:
    """
    Extract file key from a public URL.
    
    Args:
        url: The public URL
        domain: The public domain for the bucket
    
    Returns:
        File key or None if URL doesn't match domain
    """
    if not url:
        return None
        
    # Remove protocol if present
    clean_domain = domain.replace('https://', '').replace('http://', '')
    
    if clean_domain in url:
        # Split by domain and get the part after it
        parts = url.split(clean_domain)
        if len(parts) > 1:
            file_key = parts[1].lstrip('/')
            return file_key if file_key else None
    
    return None
