"""
Unit tests untuk data loader module
"""
import pytest
from pathlib import Path
from src.data.loader import DataLoader

class TestDataLoader:
    """Test cases untuk DataLoader class"""
    
    @pytest.fixture
    def loader(self):
        return DataLoader()
    
    def test_loader_initialization(self, loader):
        assert loader.data_path == Path("./database/data")
    
    def test_csv_not_found(self, loader):
        with pytest.raises(FileNotFoundError):
            loader.load_csv("nonexistent.csv")
