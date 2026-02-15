"""
Data Generator for AI-Driven Data Leakage Detection System
Generates dataset with 13 key features grouped into 5 categories
As per Research Methodology Specification
"""

import numpy as np
import pandas as pd
from datetime import datetime
import random
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR, DATASET_PATH, RANDOM_STATE

# Set random seeds for reproducibility
np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)


class DataLeakageDatasetGenerator:
    """
    Generate synthetic dataset for data leakage detection
    Features organized into 5 categories as per research methodology
    """
    
    def __init__(self, n_samples=10000, leakage_ratio=0.15):
        """
        Initialize dataset generator
        
        Args:
            n_samples: Total number of samples to generate
            leakage_ratio: Ratio of leakage instances (default 15%)
        """
        self.n_samples = n_samples
        self.n_leakage = int(n_samples * leakage_ratio)
        self.n_normal = n_samples - self.n_leakage
        
        # Define categorical values
        self.user_roles = ['employee', 'manager', 'admin', 'contractor', 'intern']
        self.departments = ['IT', 'HR', 'Finance', 'Sales', 'R&D', 'Operations']
        self.access_types = ['read', 'write', 'download', 'upload', 'copy', 'print']
        self.device_types = ['laptop', 'desktop', 'mobile', 'tablet', 'server']
        self.sensitivity_levels = ['public', 'internal', 'confidential', 'restricted']
        self.file_types = ['document', 'spreadsheet', 'code', 'database', 'image', 'archive']
        self.source_ip_categories = ['internal_trusted', 'internal_guest', 'vpn', 'external']
        self.destination_categories = ['internal_server', 'internal_storage', 'cloud_storage', 
                                      'personal_device', 'external_server', 'unknown']
    
    def generate_authentication_features(self, is_leakage=False):
        """
        Category 1: Authentication Features (3 features)
        - login_success
        - failed_login_attempts
        - privileged_account
        """
        if is_leakage:
            # Leakage scenarios often involve compromised credentials or privilege escalation
            login_success = 1 if random.random() > 0.1 else 0
            failed_login_attempts = np.random.choice([0, 1, 2, 3, 4, 5], 
                                                     p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03])
            privileged_account = 1 if random.random() > 0.6 else 0
        else:
            # Normal scenarios
            login_success = 1 if random.random() > 0.02 else 0
            failed_login_attempts = 0 if random.random() > 0.1 else np.random.choice([1, 2])
            privileged_account = 1 if random.random() > 0.85 else 0
        
        return {
            'login_success': login_success,
            'failed_login_attempts': failed_login_attempts,
            'privileged_account': privileged_account
        }
    
    def generate_behavioral_features(self, is_leakage=False):
        """
        Category 2: Behavioral Features (3 features)
        - access_frequency
        - data_volume_mb
        - session_duration_mins
        """
        if is_leakage:
            # Suspicious behavior: high frequency, large volumes, prolonged sessions
            access_frequency = np.random.randint(30, 100)
            data_volume_mb = round(np.random.uniform(500, 5000), 2)
            session_duration_mins = round(np.random.uniform(120, 600), 2)
        else:
            # Normal behavior
            access_frequency = np.random.randint(1, 35)
            data_volume_mb = round(np.random.uniform(0.1, 200), 2)
            session_duration_mins = round(np.random.uniform(5, 120), 2)
        
        return {
            'access_frequency': access_frequency,
            'data_volume_mb': data_volume_mb,
            'session_duration_mins': session_duration_mins
        }
    
    def generate_data_sensitivity_features(self, is_leakage=False):
        """
        Category 3: Data Sensitivity Features (3 features)
        - data_sensitivity_level
        - file_type
        - permission_mismatch
        """
        if is_leakage:
            # Leakage: accessing highly sensitive data with permission issues
            sensitivity_level = np.random.choice(
                self.sensitivity_levels,
                p=[0.05, 0.15, 0.35, 0.45]  # Bias towards restricted/confidential
            )
            file_type = np.random.choice(
                self.file_types,
                p=[0.1, 0.15, 0.25, 0.25, 0.05, 0.20]  # High risk types
            )
            permission_mismatch = 1 if random.random() > 0.3 else 0
        else:
            # Normal: mostly public/internal data with proper permissions
            sensitivity_level = np.random.choice(
                self.sensitivity_levels,
                p=[0.40, 0.35, 0.20, 0.05]
            )
            file_type = np.random.choice(
                self.file_types,
                p=[0.40, 0.30, 0.10, 0.05, 0.10, 0.05]
            )
            permission_mismatch = 1 if random.random() > 0.95 else 0
        
        return {
            'data_sensitivity_level': sensitivity_level,
            'file_type': file_type,
            'permission_mismatch': permission_mismatch
        }
    
    def generate_network_context_features(self, is_leakage=False):
        """
        Category 4: Network Context Features (4 features)
        - source_ip_category
        - destination_category
        - external_connection
        - encryption_used
        """
        if is_leakage:
            # Leakage: suspicious source IPs, external destinations, encryption to hide
            source_ip_category = np.random.choice(
                self.source_ip_categories,
                p=[0.3, 0.2, 0.2, 0.3]  # More external/guest IPs
            )
            destination_category = np.random.choice(
                self.destination_categories,
                p=[0.1, 0.1, 0.2, 0.3, 0.25, 0.05]  # Personal/external destinations
            )
            external_connection = 1 if random.random() > 0.3 else 0
            encryption_used = 1 if random.random() > 0.4 else 0
        else:
            # Normal: trusted internal sources, internal destinations
            source_ip_category = np.random.choice(
                self.source_ip_categories,
                p=[0.70, 0.15, 0.10, 0.05]
            )
            destination_category = np.random.choice(
                self.destination_categories,
                p=[0.50, 0.30, 0.10, 0.05, 0.03, 0.02]
            )
            external_connection = 1 if random.random() > 0.9 else 0
            encryption_used = 1 if random.random() > 0.7 else 0
        
        return {
            'source_ip_category': source_ip_category,
            'destination_category': destination_category,
            'external_connection': external_connection,
            'encryption_used': encryption_used
        }
    
    def generate_temporal_features(self, is_leakage=False):
        """
        Category 5: Temporal Features (4 features)
        - hour_of_day
        - day_of_week
        - is_weekend
        - is_business_hours
        """
        if is_leakage:
            # Leakage: off-hours, weekends
            hour = np.random.choice(
                list(range(24)),
                p=[0.08, 0.08, 0.08, 0.06, 0.06, 0.04,  # 0-5 (night)
                   0.02, 0.02, 0.02, 0.02, 0.02, 0.02,  # 6-11 (morning)
                   0.02, 0.02, 0.02, 0.02, 0.02, 0.02,  # 12-17 (afternoon)
                   0.03, 0.03, 0.04, 0.05, 0.07, 0.07]  # 18-23 (evening/night)
            )
            day_of_week = np.random.randint(0, 7)
            is_weekend = 1 if day_of_week >= 5 else 0
        else:
            # Normal: business hours, weekdays
            hour = np.random.choice(
                list(range(24)),
                p=[0.01, 0.01, 0.01, 0.01, 0.01, 0.01,  # 0-5
                   0.02, 0.03, 0.05, 0.08, 0.09, 0.09,  # 6-11
                   0.08, 0.09, 0.09, 0.08, 0.07, 0.05,  # 12-17
                   0.03, 0.02, 0.02, 0.02, 0.02, 0.01]  # 18-23
            )
            day_of_week = np.random.choice([0, 1, 2, 3, 4, 5, 6], 
                                          p=[0.18, 0.18, 0.18, 0.18, 0.18, 0.05, 0.05])
            is_weekend = 1 if day_of_week >= 5 else 0
        
        is_business_hours = 1 if (9 <= hour <= 17 and day_of_week < 5) else 0
        
        return {
            'hour_of_day': hour,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'is_business_hours': is_business_hours
        }
    
    def generate_contextual_metadata(self, is_leakage=False):
        """
        Generate additional contextual features (not part of core 13)
        - user_id, session_id
        - user_role, department
        - access_type, device_type
        """
        if is_leakage:
            user_role = np.random.choice(
                self.user_roles,
                p=[0.35, 0.25, 0.15, 0.15, 0.10]
            )
            access_type = np.random.choice(
                self.access_types,
                p=[0.05, 0.15, 0.35, 0.20, 0.15, 0.10]
            )
        else:
            user_role = np.random.choice(
                self.user_roles,
                p=[0.40, 0.25, 0.15, 0.15, 0.05]
            )
            access_type = np.random.choice(
                self.access_types,
                p=[0.45, 0.25, 0.10, 0.10, 0.05, 0.05]
            )
        
        department = random.choice(self.departments)
        device_type = random.choice(self.device_types)
        
        return {
            'user_role': user_role,
            'department': department,
            'access_type': access_type,
            'device_type': device_type
        }
    
    def generate_dataset(self):
        """Generate complete dataset with all feature categories"""
        print(f"=" * 70)
        print(f"GENERATING DATA LEAKAGE DETECTION DATASET")
        print(f"=" * 70)
        print(f"\nDataset Specification:")
        print(f"  Total Samples: {self.n_samples}")
        print(f"  Normal Instances: {self.n_normal} ({(self.n_normal/self.n_samples)*100:.1f}%)")
        print(f"  Leakage Instances: {self.n_leakage} ({(self.n_leakage/self.n_samples)*100:.1f}%)")
        print(f"\nFeature Categories:")
        print(f"  1. Authentication Features: 3")
        print(f"  2. Behavioral Features: 3")
        print(f"  3. Data Sensitivity Features: 3")
        print(f"  4. Network Context Features: 4")
        print(f"  5. Temporal Features: 4")
        print(f"  Total Core Features: 13")
        print(f"  Additional Context Features: 6")
        print(f"=" * 70)
        
        data = []
        
        # Generate normal instances
        print(f"\nGenerating {self.n_normal} normal instances...")
        for i in range(self.n_normal):
            sample = {
                'user_id': f'USER_{random.randint(1000, 9999)}',
                'session_id': f'SESSION_{i}_{random.randint(10000, 99999)}',
                **self.generate_authentication_features(is_leakage=False),
                **self.generate_behavioral_features(is_leakage=False),
                **self.generate_data_sensitivity_features(is_leakage=False),
                **self.generate_network_context_features(is_leakage=False),
                **self.generate_temporal_features(is_leakage=False),
                **self.generate_contextual_metadata(is_leakage=False),
                'is_leakage': 0
            }
            data.append(sample)
            
            if (i + 1) % 2000 == 0:
                print(f"  Progress: {i + 1}/{self.n_normal} samples generated")
        
        # Generate leakage instances
        print(f"\nGenerating {self.n_leakage} leakage instances...")
        for i in range(self.n_leakage):
            sample = {
                'user_id': f'USER_{random.randint(1000, 9999)}',
                'session_id': f'SESSION_{i+self.n_normal}_{random.randint(10000, 99999)}',
                **self.generate_authentication_features(is_leakage=True),
                **self.generate_behavioral_features(is_leakage=True),
                **self.generate_data_sensitivity_features(is_leakage=True),
                **self.generate_network_context_features(is_leakage=True),
                **self.generate_temporal_features(is_leakage=True),
                **self.generate_contextual_metadata(is_leakage=True),
                'is_leakage': 1
            }
            data.append(sample)
            
            if (i + 1) % 500 == 0:
                print(f"  Progress: {i + 1}/{self.n_leakage} samples generated")
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
        
        print(f"\n✓ Dataset generation completed successfully!")
        
        return df
    
    def save_dataset(self, df):
        """Save dataset to CSV"""
        # Ensure data directory exists
        DATA_DIR.mkdir(exist_ok=True)
        
        # Save to CSV
        df.to_csv(DATASET_PATH, index=False)
        
        print(f"\n" + "=" * 70)
        print(f"DATASET SAVED")
        print(f"=" * 70)
        print(f"Location: {DATASET_PATH}")
        print(f"Size: {len(df)} rows × {len(df.columns)} columns")
        print(f"\nColumn Names:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f"\nClass Distribution:")
        print(df['is_leakage'].value_counts())
        print(f"\nPercentage Distribution:")
        print((df['is_leakage'].value_counts(normalize=True) * 100).round(2))
        
        print(f"\nDataset Statistics:")
        print(df.describe())
        
        print(f"\n" + "=" * 70)


def main():
    """Main function to generate dataset"""
    print("\n" + "=" * 70)
    print(" " * 10 + "AI-DRIVEN DATA LEAKAGE DETECTION")
    print(" " * 15 + "DATASET GENERATOR v2.0")
    print("=" * 70)
    print("\nBased on Research Methodology Specification:")
    print("  - 13 Core Features in 5 Categories")
    print("  - Authentication, Behavioral, Data Sensitivity,")
    print("    Network Context, and Temporal Features")
    print("=" * 70)
    
    # Create generator
    generator = DataLeakageDatasetGenerator(n_samples=10000, leakage_ratio=0.15)
    
    # Generate dataset
    df = generator.generate_dataset()
    
    # Display sample
    print("\n" + "=" * 70)
    print("SAMPLE DATA (First 5 rows)")
    print("=" * 70)
    print(df.head())
    
    # Save dataset
    generator.save_dataset(df)
    
    print("\n" + "=" * 70)
    print("✓ DATASET GENERATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nDataset file: data_leakage_detection.csv")
    print(f"Location: {DATASET_PATH}")
    print(f"\nYou can now proceed to:")
    print(f"  1. Train models: python src/train_pipeline.py")
    print(f"  2. Explore data: Open notebooks/exploration.ipynb")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
