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
