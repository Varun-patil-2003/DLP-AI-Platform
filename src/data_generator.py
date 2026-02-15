"""
Data Generator for AI-Driven Data Leakage Detection System
Generates synthetic dataset with behavioral, contextual, and temporal features
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR, DATASET_PATH, RANDOM_STATE

# Set random seeds
np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)


class DataLeakageDatasetGenerator:
    """Generate synthetic dataset for data leakage detection"""
    
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
        
    def generate_temporal_features(self, is_leakage=False):
        """Generate temporal features"""
        if is_leakage:
            # Leakage more likely during off-hours
            hour = np.random.choice([0, 1, 2, 3, 4, 5, 22, 23], p=[0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.15, 0.15])
            day_of_week = np.random.randint(0, 7)
            is_weekend = 1 if day_of_week >= 5 else 0
        else:
            # Normal access during business hours
            hour = np.random.choice(range(24), p=[0.01]*6 + [0.08]*12 + [0.02]*6)
            day_of_week = np.random.randint(0, 7)
            is_weekend = 1 if day_of_week >= 5 else 0
            
        is_business_hours = 1 if (9 <= hour <= 17 and not is_weekend) else 0
        unusual_time_access = 1 if ((hour < 6 or hour > 22) or is_weekend) else 0
        
        return {
            'hour_of_day': hour,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'is_business_hours': is_business_hours,
            'unusual_time_access': unusual_time_access
        }
    
    def generate_behavioral_features(self, is_leakage=False):
        """Generate behavioral features"""
        if is_leakage:
            # Suspicious behavior patterns
            access_frequency = np.random.randint(15, 100)
            data_volume_mb = np.random.uniform(500, 5000)
            session_duration_mins = np.random.uniform(120, 600)
            multiple_devices = 1 if random.random() > 0.5 else 0
            rapid_file_access = 1 if random.random() > 0.4 else 0
            external_connection = 1 if random.random() > 0.6 else 0
        else:
            # Normal behavior patterns
            access_frequency = np.random.randint(1, 30)
            data_volume_mb = np.random.uniform(1, 200)
            session_duration_mins = np.random.uniform(10, 120)
            multiple_devices = 1 if random.random() > 0.8 else 0
            rapid_file_access = 1 if random.random() > 0.9 else 0
            external_connection = 1 if random.random() > 0.95 else 0
            
        return {
            'access_frequency': access_frequency,
            'data_volume_mb': round(data_volume_mb, 2),
            'session_duration_mins': round(session_duration_mins, 2),
            'multiple_devices': multiple_devices,
            'rapid_file_access': rapid_file_access,
            'external_connection': external_connection
        }
    
    def generate_contextual_features(self, is_leakage=False):
        """Generate contextual features"""
        if is_leakage:
            # Higher sensitivity data accessed
            sensitivity_level = np.random.choice(
                self.sensitivity_levels, 
                p=[0.05, 0.15, 0.35, 0.45]
            )
            user_role = np.random.choice(
                self.user_roles,
                p=[0.35, 0.25, 0.15, 0.15, 0.10]
            )
            access_type = np.random.choice(
                self.access_types,
                p=[0.05, 0.15, 0.35, 0.20, 0.15, 0.10]
            )
        else:
            # Normal access patterns
            sensitivity_level = np.random.choice(
                self.sensitivity_levels,
                p=[0.40, 0.35, 0.20, 0.05]
            )
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
        file_type = random.choice(self.file_types)
        
        # Permission mismatch (higher for leakage)
        permission_mismatch = 1 if random.random() > (0.7 if is_leakage else 0.95) else 0
        
        return {
            'user_role': user_role,
            'department': department,
            'data_sensitivity_level': sensitivity_level,
            'access_type': access_type,
            'device_type': device_type,
            'file_type': file_type,
            'permission_mismatch': permission_mismatch
        }
    
    def generate_user_features(self, is_leakage=False):
        """Generate user-specific features"""
        if is_leakage:
            days_since_last_access = np.random.randint(0, 30)
            failed_login_attempts = np.random.randint(0, 5)
            privileged_account = 1 if random.random() > 0.6 else 0
        else:
            days_since_last_access = np.random.randint(0, 7)
            failed_login_attempts = 0 if random.random() > 0.1 else np.random.randint(1, 2)
            privileged_account = 1 if random.random() > 0.85 else 0
            
        return {
            'days_since_last_access': days_since_last_access,
            'failed_login_attempts': failed_login_attempts,
            'privileged_account': privileged_account
        }
    
    def generate_network_features(self, is_leakage=False):
        """Generate network-related features"""
        if is_leakage:
            unusual_destination = 1 if random.random() > 0.4 else 0
            encryption_used = 1 if random.random() > 0.5 else 0
            vpn_usage = 1 if random.random() > 0.3 else 0
        else:
            unusual_destination = 1 if random.random() > 0.95 else 0
            encryption_used = 1 if random.random() > 0.3 else 0
            vpn_usage = 1 if random.random() > 0.8 else 0
            
        return {
            'unusual_destination': unusual_destination,
            'encryption_used': encryption_used,
            'vpn_usage': vpn_usage
        }
    
    def generate_dataset(self):
        """Generate complete dataset"""
        print(f"Generating dataset with {self.n_samples} samples...")
        print(f"Normal instances: {self.n_normal}")
        print(f"Leakage instances: {self.n_leakage}")
        
        data = []
        
        # Generate normal instances
        for i in range(self.n_normal):
            sample = {
                'user_id': f'USER_{random.randint(1000, 9999)}',
                'session_id': f'SESSION_{i}_{random.randint(10000, 99999)}',
                **self.generate_temporal_features(is_leakage=False),
                **self.generate_behavioral_features(is_leakage=False),
                **self.generate_contextual_features(is_leakage=False),
                **self.generate_user_features(is_leakage=False),
                **self.generate_network_features(is_leakage=False),
                'is_leakage': 0
            }
            data.append(sample)
        
        # Generate leakage instances
        for i in range(self.n_leakage):
            sample = {
                'user_id': f'USER_{random.randint(1000, 9999)}',
                'session_id': f'SESSION_{i+self.n_normal}_{random.randint(10000, 99999)}',
                **self.generate_temporal_features(is_leakage=True),
                **self.generate_behavioral_features(is_leakage=True),
                **self.generate_contextual_features(is_leakage=True),
                **self.generate_user_features(is_leakage=True),
                **self.generate_network_features(is_leakage=True),
                'is_leakage': 1
            }
            data.append(sample)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
        
        return df
    
    def save_dataset(self, df):
        """Save dataset to CSV"""
        DATA_DIR.mkdir(exist_ok=True)
        df.to_csv(DATASET_PATH, index=False)
        print(f"\n✓ Dataset saved to: {DATASET_PATH}")
        print(f"✓ Total samples: {len(df)}")
        print(f"✓ Features: {len(df.columns)}")
        print(f"\nClass Distribution:")
        print(df['is_leakage'].value_counts())
        print(f"\nDataset shape: {df.shape}")


def main():
    """Main function to generate dataset"""
    print("=" * 70)
    print("AI-DRIVEN DATA LEAKAGE DETECTION - DATASET GENERATOR")
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
    
    print("\n" + "=" * 70)
    print("DATASET STATISTICS")
    print("=" * 70)
    print(df.describe())
    
    # Save dataset
    generator.save_dataset(df)
    
    print("\n" + "=" * 70)
    print("✓ Dataset generation completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
