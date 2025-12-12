#!/bin/bash

# ============================================================================
# Setup Script untuk Dashboard Universitas - Data Insight Project
# Nama Project: 
# Deskripsi: Inisialisasi struktur project dan environment setup
# Author: Data Insight Student
# Date: December 2025
# ============================================================================

set -e  # Exit jika ada error

# Color codes untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FUNGSI HELPER
# ============================================================================

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# ============================================================================
# TAHAP 1: CEK PREREQUISITES
# ============================================================================

print_header "TAHAP 1: Cek Prerequisites"

# Cek Python installation
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
else
    # Try alternative method for Windows
    if command -v py &> /dev/null; then
        PYTHON_CMD="py"
        PYTHON_VERSION=$(py --version 2>&1 | awk '{print $2}')
    else
        print_error "Python tidak terinstall. Silakan install Python 3.9 atau lebih tinggi."
        exit 1
    fi
fi

print_success "Python $PYTHON_VERSION terdeteksi"

# Cek pip installation
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    # Try using Python to run pip
    if $PYTHON_CMD -m pip --version > /dev/null 2>&1; then
        PIP_CMD="$PYTHON_CMD -m pip"
    else
        print_error "pip tidak terinstall. Silakan install pip."
        exit 1
    fi
fi

print_success "pip terdeteksi"

# Cek git installation
if ! command -v git &> /dev/null; then
    print_info "Git tidak terinstall. Beberapa fitur akan terbatas."
else
    print_success "Git terdeteksi"
fi

# ============================================================================
# TAHAP 2: BUAT STRUKTUR DIREKTORI
# ============================================================================

print_header "TAHAP 2: Membuat Struktur Direktori Project"

PROJECT_NAME="dashboard universitas islam indonesia"
PROJECT_DIR=$(pwd)

# Buat main directories
DIRS=(
    ".venv"
    "src"
    "src/dashboard"
    "src/data"
    "src/utils"
    "notebooks"
    "docs"
    "database"
    "database/data"
    "database/schemas"
    "images"
    "images/screenshots"
    "images/mockups"
    "output"
    "output/reports"
    "output/exports"
    "tests"
    "config"
    ".github/workflows"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$PROJECT_DIR/$dir"
    if [ $? -eq 0 ]; then
        print_success "Direktori dibuat: $dir"
    else
        print_error "Gagal membuat direktori: $dir"
        exit 1
    fi
done

# ============================================================================
# TAHAP 3: SETUP PYTHON VIRTUAL ENVIRONMENT
# ============================================================================

print_header "TAHAP 3: Setup Python Virtual Environment"

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]] || [[ "$OS" == "Windows_NT" ]]; then
        echo "windows"
    else
        echo "unix"
    fi
}

OS_TYPE=$(detect_os)

# Check if virtual environment exists properly
if [ "$OS_TYPE" = "windows" ]; then
    # Windows
    if [ -f ".venv/Scripts/activate" ]; then
        print_info "Virtual environment Windows sudah ada. Menggunakan existing environment..."
    else
        print_info "Membuat virtual environment Windows..."
        # For Windows, try different approaches to avoid the alias issue
        if [ "$PYTHON_CMD" = "py" ]; then
            py -m venv .venv 2>/dev/null || python -m venv .venv
        else
            $PYTHON_CMD -m venv .venv 2>/dev/null || python -m venv .venv
        fi
        print_success "Virtual environment Windows dibuat"
    fi
    source .venv/Scripts/activate
else
    # Unix/Linux/macOS
    if [ -f ".venv/bin/activate" ]; then
        print_info "Virtual environment Unix sudah ada. Menggunakan existing environment..."
    else
        print_info "Membuat virtual environment Unix..."
        $PYTHON_CMD -m venv .venv
        print_success "Virtual environment Unix dibuat"
    fi
    source .venv/bin/activate
fi
print_success "Virtual environment diaktifkan"

# Upgrade pip, setuptools, wheel
print_info "Upgrade pip, setuptools, dan wheel..."
# Upgrade pip, setuptools, wheel
print_info "Upgrade pip, setuptools, dan wheel..."
if [ "$OS_TYPE" = "windows" ]; then
    # For Windows, use Python directly to avoid some issues
    python -m pip install --upgrade pip setuptools wheel || echo "Lanjutkan meskipun ada error upgrade pip"
else
    $PIP_CMD install --upgrade pip setuptools wheel
fi
print_success "pip, setuptools, dan wheel di-upgrade"

# ============================================================================
# TAHAP 4: INSTALL DEPENDENCIES
# ============================================================================

print_header "TAHAP 4: Install Dependencies"

# Buat requirements.txt
cat > requirements.txt << 'EOF'
# Dashboard & Web Framework
streamlit>=1.28.1
dash>=2.14.1
plotly>=5.18.0
panel>=1.3.0

# Data Processing
pandas>=2.2.0
numpy>=1.26.2
scipy>=1.11.3

# Database
sqlalchemy>=2.0.23
# Removed sqlite3-python as it's not a valid package; sqlite3 is built into Python
pymongo>=4.6.0

# Data Visualization
matplotlib>=3.8.1
seaborn>=0.13.0
altair>=5.1.2
folium>=0.14.0

# Machine Learning & Analytics
scikit-learn>=1.3.2
statsmodels>=0.14.0

# Data Loading & Sources
kaggle>=1.5.13
requests>=2.31.0

# Utilities
python-dotenv>=1.0
colorama>=0.4.6
tqdm>=4.66.1

# Testing
pytest>=7.4.3
pytest-cov>=4.1.0

# Code Quality
black>=23.11.0
flake8>=6.1.0
pylint>=3.0.2

# Jupyter & Notebooks
jupyter>=1.0.0
ipython>=8.17.2
ipykernel>=6.26.0
notebook>=7.0.6

# Documentation
sphinx>=7.2.6
sphinx-rtd-theme>=2.0.0

# Development
python-dateutil>=2.8.2
pytz>=2023.3
EOF

print_success "requirements.txt dibuat"

# Install dependencies
print_info "Menginstall dependencies (ini mungkin memakan waktu beberapa menit)..."
if [ "$OS_TYPE" = "windows" ]; then
    # For Windows, install packages one by one to handle errors better
    while read requirement; do
        # Skip empty lines and comments
        if [[ -z "$requirement" || "$requirement" =~ ^[[:space:]]*# ]]; then
            continue
        fi
        
        print_info "Menginstall: $requirement"
        if $PIP_CMD install "$requirement" --only-binary=all; then
            print_success "✓ $requirement berhasil diinstall"
        else
            print_error "✗ Gagal menginstall $requirement, mencoba tanpa batasan binary..."
            if $PIP_CMD install "$requirement"; then
                print_success "✓ $requirement berhasil diinstall (tanpa batasan binary)"
            else
                print_error "✗ Gagal menginstall $requirement (kemungkinan tidak kompatibel di Windows)"
            fi
        fi
    done < requirements.txt
else
    $PIP_CMD install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Semua dependencies berhasil diinstall"
    else
        print_error "Gagal menginstall beberapa dependencies"
        exit 1
    fi
fi

print_success "Dependencies selesai diinstall (dengan atau tanpa error)"

# ============================================================================
# TAHAP 5: BUAT FILE KONFIGURASI & TEMPLATE
# ============================================================================

print_header "TAHAP 5: Buat File Konfigurasi dan Template"

# Config file (.env)
cat > .env << 'EOF'
# Database Configuration
DB_TYPE=sqlite
DB_PATH=./database/university.db

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info

# Data Configuration
DATA_SOURCE=local  # local, kaggle, or api
DATA_PATH=./database/data

# App Configuration
APP_TITLE="University Analytics Dashboard"
APP_VERSION=1.0.0
DEBUG=False

# Kaggle API (jika menggunakan Kaggle data)
# KAGGLE_USERNAME=your_username
# KAGGLE_KEY=your_api_key
EOF

print_success ".env file dibuat"

# Config Python
cat > config/config.py << 'EOF'
"""
Configuration module untuk University Dashboard
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    APP_TITLE = os.getenv("APP_TITLE", "University Analytics Dashboard")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
class DatabaseConfig:
    """Database configuration"""
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_PATH = os.getenv("DB_PATH", "./database/university.db")
    
class StreamlitConfig:
    """Streamlit-specific configuration"""
    SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))
    LOGGER_LEVEL = os.getenv("STREAMLIT_LOGGER_LEVEL", "info")

class DataConfig:
    """Data configuration"""
    DATA_SOURCE = os.getenv("DATA_SOURCE", "local")
    DATA_PATH = os.getenv("DATA_PATH", "./database/data")
EOF

print_success "config/config.py dibuat"

# Main app template
cat > src/dashboard/app.py << 'EOF'
"""
Main Dashboard Application
University Analytics Dashboard - Streamlit Version
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="University Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Navigation")
    
    page = st.sidebar.radio(
        "Select Page:",
        ["🏠 Home", "📈 Overview", "👥 Student Analytics", "📚 Academic Programs", "💰 Finance", "⚙️ Settings"]
    )
    
    # Main content
    if page == "🏠 Home":
        st.title("🎓 University Analytics Dashboard")
        st.write("""
            Welcome to the University Analytics Dashboard!
            
            This dashboard provides comprehensive insights into university operations,
            student demographics, academic performance, and financial metrics.
        """)
        
    elif page == "📈 Overview":
        st.title("📈 Overview")
        st.info("Overview page - Coming soon!")
        
    elif page == "👥 Student Analytics":
        st.title("👥 Student Analytics")
        st.info("Student Analytics page - Coming soon!")
        
    elif page == "📚 Academic Programs":
        st.title("📚 Academic Programs")
        st.info("Academic Programs page - Coming soon!")
        
    elif page == "💰 Finance":
        st.title("💰 Finance")
        st.info("Finance page - Coming soon!")
        
    elif page == "⚙️ Settings":
        st.title("⚙️ Settings")
        st.info("Settings page - Coming soon!")

if __name__ == "__main__":
    main()
EOF

print_success "src/dashboard/app.py dibuat"

# __init__.py files
touch src/__init__.py
touch src/dashboard/__init__.py
touch src/data/__init__.py
touch src/utils/__init__.py

print_success "__init__.py files dibuat"

# Data utilities template
cat > src/data/loader.py << 'EOF'
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
EOF

print_success "src/data/loader.py dibuat"

# Database schema template
cat > database/schemas/schema.sql << 'EOF'
-- ============================================================================
-- University Database Schema
-- ============================================================================

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    enrollment_date DATE,
    major_id INTEGER,
    gpa DECIMAL(3,2),
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (major_id) REFERENCES programs(program_id)
);

-- Programs/Majors table
CREATE TABLE IF NOT EXISTS programs (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_name VARCHAR(255) NOT NULL,
    faculty_id INTEGER,
    program_type VARCHAR(50),
    student_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

-- Faculty table
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    specialization VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) UNIQUE,
    credits INTEGER,
    program_id INTEGER,
    faculty_id INTEGER,
    semester VARCHAR(50),
    capacity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

-- Enrollments table
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    semester VARCHAR(50),
    grade VARCHAR(2),
    score DECIMAL(5,2),
    status VARCHAR(50) DEFAULT 'ENROLLED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_programs_faculty ON programs(faculty_id);
CREATE INDEX idx_courses_program ON courses(program_id);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
EOF

print_success "database/schemas/schema.sql dibuat"

# ============================================================================
# TAHAP 6: BUAT DOCUMENTATION FILES
# ============================================================================

print_header "TAHAP 6: Buat Documentation Files"

# README
cat > README.md << 'EOF'
# University Analytics Dashboard

## 📋 Deskripsi Project

Dashboard analytics untuk universitas yang menampilkan insights tentang:
- Student enrollment dan demographics
- Academic program performance
- Faculty statistics
- Financial metrics
- Course statistics

## 🎯 Objectives

Sesuai dengan tugas mata kuliah Data Insight:
1. Evaluasi kritis dashboard existing (Montana University System)
2. Perancangan dan implementasi dashboard universitas sendiri
3. Menggunakan Python dengan framework modern (Streamlit/Dash)

## 🚀 Quick Start

### Prasyarat
- Python 3.9+
- pip atau conda
- Git (optional)

### Installation

```bash
# Clone atau download project ini
cd dashboard universitas islam indonesia

# Run setup script
chmod +x setup.sh
./setup.sh

# Atau manual setup
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# atau
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Running the Dashboard

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Streamlit app
streamlit run src/dashboard/app.py
```

Aplikasi akan berjalan di: `http://localhost:8501`

## 📁 Project Structure

```
dashboard universitas islam indonesia/
├── .venv/                      # Virtual environment
├── src/                        # Source code
│   ├── dashboard/              # Dashboard applications
│   │   └── app.py             # Main Streamlit app
│   ├── data/                  # Data processing
│   │   └── loader.py          # Data loading utilities
│   └── utils/                 # Utility functions
├── notebooks/                 # Jupyter notebooks
├── docs/                      # Documentation
├── database/                  # Database files
│   ├── data/                  # Data files (.csv, .xlsx)
│   └── schemas/               # Database schemas
├── images/                    # Project images
│   ├── screenshots/           # Dashboard screenshots
│   └── mockups/              # UI mockups
├── output/                    # Generated outputs
│   ├── reports/              # Reports
│   └── exports/              # Data exports
├── tests/                     # Unit tests
├── config/                    # Configuration files
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
├── setup.sh                  # Setup script
└── README.md                 # This file
```

## 📊 Dashboard Pages

1. **Home** - Landing page
2. **Overview** - High-level KPIs and metrics
3. **Student Analytics** - Student enrollment and demographics
4. **Academic Programs** - Program performance and statistics
5. **Finance** - Financial metrics and budgets
6. **Settings** - Dashboard configuration

## 📚 Data Sources

- Local CSV/Excel files
- Kaggle datasets
- Public university APIs
- Simulated data

## 🛠 Technologies Used

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Database**: SQLite, SQLAlchemy
- **Testing**: Pytest
- **Version Control**: Git

## 👥 Team Members

- [Your Name] - Data Scientist

## 📝 Tasks

- [ ] Complete data exploration
- [ ] Design dashboard layouts
- [ ] Implement core visualizations
- [ ] Add interactive filters
- [ ] Performance optimization
- [ ] Testing & QA
- [ ] Deployment

## 🔗 Links

- [Project Repository](#)
- [Kaggle Dataset](#)
- [Montana University Dashboard](https://mus.edu)

## 📧 Contact

For questions or feedback, contact: your.email@university.edu

## 📄 License

This project is for educational purposes (Data Insight Course).

---

**Last Updated**: December 2025
**Version**: 1.0.0
EOF

print_success "README.md dibuat"

# CONTRIBUTING.md
cat > docs/CONTRIBUTING.md << 'EOF'
# Contributing Guidelines

Panduan untuk berkontribusi pada University Analytics Dashboard project.

## Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test your changes: `pytest`
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature/your-feature`
6. Submit a Pull Request

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and modular

## Testing

Run tests before committing:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```
EOF

print_success "docs/CONTRIBUTING.md dibuat"

# .gitignore
cat > .gitignore << 'EOF'
# Virtual Environment
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Streamlit
.streamlit/
cache/

# Database
*.db
*.sqlite
*.sqlite3

# Data files
database/data/*.csv
database/data/*.xlsx

# Environment variables
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Output
output/exports/*
output/reports/*

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/
EOF

print_success ".gitignore dibuat"

# ============================================================================
# TAHAP 7: BUAT SAMPLE NOTEBOOK
# ============================================================================

print_header "TAHAP 7: Buat Sample Jupyter Notebook"

cat > notebooks/01_data_exploration.ipynb << 'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration - University Analytics\n",
    "\n",
    "This notebook explores the university dataset and prepares it for dashboard visualization."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from pathlib import Path\n",
    "\n",
    "# Set style\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 6)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load sample data\n",
    "# df = pd.read_csv('../database/data/students.csv')\n",
    "# df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Summary"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# df.info()\n",
    "# df.describe()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

print_success "notebooks/01_data_exploration.ipynb dibuat"

# ============================================================================
# TAHAP 8: BUAT TEST FILES
# ============================================================================

print_header "TAHAP 8: Buat Test Files"

cat > tests/test_data_loader.py << 'EOF'
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
EOF

print_success "tests/test_data_loader.py dibuat"

# ============================================================================
# TAHAP 9: BUAT HELPER SCRIPTS
# ============================================================================

print_header "TAHAP 9: Buat Helper Scripts"

# Run script
cat > run.sh << 'EOF'
#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Run Streamlit app
echo "Starting University Analytics Dashboard..."
echo "Dashboard akan berjalan di: http://localhost:8501"
echo ""
echo "Tekan Ctrl+C untuk menghentikan..."

streamlit run src/dashboard/app.py
EOF

chmod +x run.sh
print_success "run.sh dibuat dan dijalankan"

# Generate sample data script
mkdir -p scripts
cat > scripts/generate_sample_data.py << 'EOF'
"""
Generate sample data untuk testing
"""
import pandas as pd
import numpy as np
from pathlib import Path

def generate_sample_data():
    """Generate sample university data"""
    
    # Create data directory
    Path("database/data").mkdir(parents=True, exist_ok=True)
    
    # Generate sample students data
    np.random.seed(42)
    students = pd.DataFrame({
        'student_id': range(1, 101),
        'student_name': [f'Student_{i}' for i in range(1, 101)],
        'major': np.random.choice(['Computer Science', 'Business', 'Engineering', 'Arts'], 100),
        'gpa': np.random.uniform(2.0, 4.0, 100),
        'enrollment_year': np.random.choice([2021, 2022, 2023], 10),
        'status': np.random.choice(['ACTIVE', 'GRADUATED', 'INACTIVE'], 100)
    })
    
    students.to_csv('database/data/students.csv', index=False)
    print("✓ Sample students data saved to database/data/students.csv")
    
    # Generate sample programs data
    programs = pd.DataFrame({
        'program_id': range(1, 11),
        'program_name': ['Computer Science', 'Business', 'Engineering', 'Arts',
                        'Science', 'Medicine', 'Law', 'Education', 'Agriculture', 'Architecture'],
        'student_count': np.random.randint(50, 300, 10),
        'faculty_count': np.random.randint(5, 30, 10)
    })
    
    programs.to_csv('database/data/programs.csv', index=False)
    print("✓ Sample programs data saved to database/data/programs.csv")

if __name__ == "__main__":
    generate_sample_data()
    print("\nSample data generation complete!")
EOF

chmod +x scripts/generate_sample_data.py
print_success "scripts/generate_sample_data.py dibuat"

# ============================================================================
# TAHAP 10: FINALISASI
# ============================================================================

print_header "TAHAP 10: Finalisasi Setup"

# Create a summary file
cat > SETUP_SUMMARY.txt << 'EOF'
================================================================================
UNIVERSITY DASHBOARD SETUP SUMMARY
================================================================================

Setup Date: $(date)
Setup Location: $(pwd)

PROJECT STRUCTURE CREATED:
✓ .venv/              - Python virtual environment
✓ src/                - Source code
✓ notebooks/          - Jupyter notebooks
✓ docs/               - Documentation
✓ database/           - Database files and schemas
✓ images/             - Project images
✓ output/             - Generated outputs
✓ tests/              - Unit tests
✓ config/             - Configuration files
✓ scripts/            - Utility scripts

FILES CREATED:
✓ requirements.txt    - Python dependencies
✓ .env                - Environment variables
✓ .gitignore          - Git ignore patterns
✓ README.md           - Main documentation
✓ setup.sh            - Setup script
✓ run.sh              - Run script
✓ config/config.py    - Configuration module
✓ src/dashboard/app.py - Main Streamlit app
✓ src/data/loader.py  - Data loading utilities
✓ database/schemas/schema.sql - Database schema
✓ notebooks/01_data_exploration.ipynb - Sample notebook
✓ tests/test_data_loader.py - Unit tests
✓ scripts/generate_sample_data.py - Sample data generator

NEXT STEPS:
1. Activate virtual environment: source .venv/bin/activate
2. Generate sample data: python scripts/generate_sample_data.py
3. Run dashboard: ./run.sh atau streamlit run src/dashboard/app.py
4. Open browser: http://localhost:8501

USEFUL COMMANDS:
- Run tests: pytest tests/
- Code format: black src/
- Code quality: flake8 src/
- Start notebook: jupyter notebook
- Deactivate venv: deactivate

DOCUMENTATION:
- README.md - Project overview and quick start
- docs/CONTRIBUTING.md - Contributing guidelines
- docs/ - Additional documentation

For more information, see README.md

================================================================================
EOF

cat SETUP_SUMMARY.txt

print_success "SETUP_SUMMARY.txt dibuat"

# ============================================================================
# FINISH
# ============================================================================

print_header "✅ SETUP SELESAI!"

echo -e "${GREEN}Project '${PROJECT_NAME}' berhasil di-setup!${NC}\n"

echo "Next Steps:"
echo "1. Activate virtual environment:"
echo -e "   ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo "2. Generate sample data (optional):"
echo -e "   ${YELLOW}python scripts/generate_sample_data.py${NC}"
echo ""
echo "3. Run dashboard:"
echo -e "   ${YELLOW}./run.sh${NC}"
echo "   atau"
echo -e "   ${YELLOW}streamlit run src/dashboard/app.py${NC}"
echo ""
echo "4. Open browser: http://localhost:8501"
echo ""
echo -e "${BLUE}Happy coding! 🚀${NC}"
echo ""
