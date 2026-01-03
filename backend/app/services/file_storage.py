import os
import shutil
from fastapi import UploadFile
from typing import List, Optional
from ..core.config import settings
import uuid
import logging

logger = logging.getLogger(__name__)


class FileStorageService:
    """
    Service for handling file uploads (images and audio)
    Stores files locally in /uploads directory
    
    For production: Replace with Cloudinary, AWS S3, or Azure Blob Storage
    """
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create upload directories if they don't exist"""
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(f"{self.upload_dir}/images", exist_ok=True)
        os.makedirs(f"{self.upload_dir}/audio", exist_ok=True)
        logger.info(f"✅ Upload directories ready: {self.upload_dir}")
    
    async def save_file(self, file: UploadFile, file_type: str = "image") -> str:
        """
        Save uploaded file to local storage
        
        Args:
            file: UploadFile object from FastAPI
            file_type: Type of file ('image' or 'audio')
        
        Returns:
            str: Public URL of the saved file
        
        Raises:
            Exception: If file save fails
        """
        try:
            # Extract file extension
            file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Determine folder based on type
            folder = f"{self.upload_dir}/{file_type}s"
            file_path = f"{folder}/{unique_filename}"
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Generate public URL (relative path)
            public_url = f"/uploads/{file_type}s/{unique_filename}"
            
            logger.info(f"✅ File saved: {public_url} (size: {os.path.getsize(file_path)} bytes)")
            return public_url
        
        except Exception as e:
            logger.error(f"❌ File upload failed: {e}")
            raise
        finally:
            file.file.close()
    
    async def save_files(self, files: List[UploadFile], file_type: str = "image") -> List[dict]:
        """
        Save multiple files
        
        Args:
            files: List of UploadFile objects
            file_type: Type of files ('image' or 'audio')
        
        Returns:
            List[dict]: List of attachment dictionaries with type and url
        """
        results = []
        for file in files:
            url = await self.save_file(file, file_type)
            results.append({"type": file_type, "url": url})
        return results
    
    def delete_file(self, file_url: str) -> bool:
        """
        Delete a file from storage
        
        Args:
            file_url: Public URL of the file (e.g., /uploads/images/abc.jpg)
        
        Returns:
            bool: True if deleted successfully
        """
        try:
            # Convert URL to file path
            file_path = file_url.replace("/uploads/", f"{self.upload_dir}/")
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"✅ File deleted: {file_url}")
                return True
            else:
                logger.warning(f"⚠️ File not found: {file_url}")
                return False
        
        except Exception as e:
            logger.error(f"❌ File deletion failed: {e}")
            return False


# Create singleton instance
file_storage_service = FileStorageService()
