import pytest
import tempfile
import os
from news_app.services.database import DatabaseService

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    
    # Create database service with temp file
    db_service = DatabaseService(temp_file.name)
    
    yield db_service
    
    # Cleanup
    os.unlink(temp_file.name)