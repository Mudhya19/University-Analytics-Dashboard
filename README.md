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
