import io
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.infrastructure.bucket import R2BucketManager
from src.shared.dependencies.auth import get_current_user
from src.shared.models.user import User
from src.shared.exceptions import FileUploadError

router = APIRouter(prefix="/uploads", tags=["uploads"])

# Allowed image types
ALLOWED_IMAGE_TYPES = {
    "image/jpeg", "image/jpg", "image/png", 
    "image/gif", "image/webp", "image/svg+xml"
}

# Maximum file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024):.1f}MB"
        )


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    path: str = Form(default="images"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a single image to R2 bucket."""
    try:
        # Validate file
        validate_image_file(file)
        
        # Read file content
        content = await file.read()
        file_buffer = io.BytesIO(content)
        
        # Initialize bucket manager
        bucket_manager = R2BucketManager()
        
        # Upload file
        file_key = await bucket_manager.put(
            path=path,
            file_buffer=file_buffer,
            content_type=file.content_type,
            file_type=file.content_type
        )
        
        # Get public URL
        public_url = bucket_manager.get_public_url(file_key)
        
        return {
            "success": True,
            "file_key": file_key,
            "url": public_url,
            "content_type": file.content_type,
            "size": len(content)
        }
        
    except FileUploadError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/images")
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    path: str = Form(default="images"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload multiple images to R2 bucket."""
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 files allowed per upload"
        )
    
    results = []
    bucket_manager = R2BucketManager()
    
    for file in files:
        try:
            # Validate file
            validate_image_file(file)
            
            # Read file content
            content = await file.read()
            file_buffer = io.BytesIO(content)
            
            # Upload file
            file_key = await bucket_manager.put(
                path=path,
                file_buffer=file_buffer,
                content_type=file.content_type,
                file_type=file.content_type
            )
            
            # Get public URL
            public_url = bucket_manager.get_public_url(file_key)
            
            results.append({
                "success": True,
                "filename": file.filename,
                "file_key": file_key,
                "url": public_url,
                "content_type": file.content_type,
                "size": len(content)
            })
            
        except FileUploadError as e:
            results.append({
                "success": False,
                "filename": file.filename,
                "error": str(e)
            })
        except Exception as e:
            results.append({
                "success": False,
                "filename": file.filename,
                "error": f"Upload failed: {str(e)}"
            })
    
    return {
        "results": results,
        "total": len(files),
        "successful": len([r for r in results if r["success"]]),
        "failed": len([r for r in results if not r["success"]])
    }


@router.delete("/image/{file_key:path}")
async def delete_image(
    file_key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an image from R2 bucket."""
    try:
        bucket_manager = R2BucketManager()
        bucket_manager.delete([file_key])
        
        return {
            "success": True,
            "message": "Image deleted successfully",
            "file_key": file_key
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )


@router.get("/image/{file_key:path}/url")
async def get_image_url(
    file_key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get public URL for an image."""
    try:
        bucket_manager = R2BucketManager()
        public_url = bucket_manager.get_public_url(file_key)
        
        return {
            "success": True,
            "file_key": file_key,
            "url": public_url
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get URL: {str(e)}"
        )
