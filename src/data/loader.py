"""
Data Loading Module
"""
import pandas as pd
from pathlib import Path
from typing import Union

class DataLoader:
    """Handle data loading operations"""
    
    def __init__(self, data_path: str = "./database/data"):
        self.data_path = Path(data_path)
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load CSV file"""
        file_path = self.data_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return pd.read_csv(file_path)
    
    def load_excel(self, filename: str, sheet_name: str = 0) -> pd.DataFrame:
        """Load Excel file"""
        file_path = self.data_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return pd.read_excel(file_path, sheet_name=sheet_name)
    
    def save_csv(self, df: pd.DataFrame, filename: str) -> None:
        """Save DataFrame to CSV"""
        file_path = self.data_path / filename
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
