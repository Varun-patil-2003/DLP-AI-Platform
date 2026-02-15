"""
Feature Engineering Module
Creates advanced features for improved model performance
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))


class FeatureEngineer:
    """Engineer advanced features from raw data"""
    
    def __init__(self):
        self.engineered_features = []
    
    def create_risk_score_features(self, df):
        """Create risk score based on multiple factors"""
        df_new = df.copy()
        
        # Behavioral risk score
        df_new['behavioral_risk_score'] = (
            (df['access_frequency'] > df['access_frequency'].quantile(0.75)).astype(int) * 0.3 +
            (df['data_volume_mb'] > df['data_volume_mb'].quantile(0.75)).astype(int) * 0.4 +
            (df['session_duration_mins'] > df['session_duration_mins'].quantile(0.75)).astype(int) * 0.3
        )
        
        # Temporal risk score
        df_new['temporal_risk_score'] = (
            df['unusual_time_access'] * 0.5 +
            (1 - df['is_business_hours']) * 0.3 +
            df['is_weekend'] * 0.2
        )
        
        # Contextual risk score (if sensitivity level exists)
        if 'data_sensitivity_level' in df.columns:
            sensitivity_map = {'public': 0, 'internal': 0.3, 'confidential': 0.6, 'restricted': 1.0}
            df_new['sensitivity_numeric'] = df['data_sensitivity_level'].map(sensitivity_map).fillna(0.5)
            
            df_new['contextual_risk_score'] = (
                df_new['sensitivity_numeric'] * 0.5 +
                df.get('permission_mismatch', 0) * 0.3 +
                df.get('external_connection', 0) * 0.2
            )
        
        self.engineered_features.extend([
            'behavioral_risk_score', 
            'temporal_risk_score', 
            'contextual_risk_score'
        ])
        
        return df_new
    
    def create_interaction_features(self, df):
        """Create interaction features"""
        df_new = df.copy()
        
        # Volume per session duration
        df_new['volume_per_minute'] = df['data_volume_mb'] / (df['session_duration_mins'] + 1)
        
        # Access frequency per day
        df_new['access_intensity'] = df['access_frequency'] / 24.0
        
        # Unusual access pattern
        df_new['unusual_pattern'] = (
            df['unusual_time_access'] * df['access_frequency']
        ) / 10.0
        
        self.engineered_features.extend([
            'volume_per_minute',
            'access_intensity',
            'unusual_pattern'
        ])
        
        return df_new
    
    def create_aggregation_features(self, df):
        """Create aggregation features based on user behavior"""
        df_new = df.copy()
        
        if 'user_id' in df.columns:
            # User-level aggregations
            user_stats = df.groupby('user_id').agg({
                'data_volume_mb': ['mean', 'std', 'max'],
                'access_frequency': ['mean', 'std'],
                'session_duration_mins': ['mean', 'std']
            }).reset_index()
            
            # Flatten column names
            user_stats.columns = ['user_id'] + [
                f'user_{col[0]}_{col[1]}' for col in user_stats.columns[1:]
            ]
            
            # Merge back
            df_new = df_new.merge(user_stats, on='user_id', how='left')
            
            # Fill NaN with 0 for first-time users
            for col in user_stats.columns:
                if col != 'user_id':
                    df_new[col].fillna(0, inplace=True)
                    self.engineered_features.append(col)
        
        return df_new
    
    def create_temporal_features(self, df):
        """Create advanced temporal features"""
        df_new = df.copy()
        
        # Time of day category
        def categorize_time(hour):
            if 6 <= hour < 12:
                return 1  # Morning
            elif 12 <= hour < 18:
                return 2  # Afternoon
            elif 18 <= hour < 22:
                return 3  # Evening
            else:
                return 4  # Night
        
        if 'hour_of_day' in df.columns:
            df_new['time_category'] = df['hour_of_day'].apply(categorize_time)
            self.engineered_features.append('time_category')
        
        # Weekday vs weekend with time
        if 'is_weekend' in df.columns and 'hour_of_day' in df.columns:
            df_new['weekend_night'] = df['is_weekend'] * (df['hour_of_day'] < 6).astype(int)
            self.engineered_features.append('weekend_night')
        
        return df_new
    
    def create_anomaly_indicators(self, df):
        """Create anomaly indicator features"""
        df_new = df.copy()
        
        # Multiple suspicious indicators
        suspicious_cols = [
            'multiple_devices', 'rapid_file_access', 'external_connection',
            'permission_mismatch', 'unusual_destination', 'unusual_time_access'
        ]
        
        available_cols = [col for col in suspicious_cols if col in df.columns]
        
        if available_cols:
            df_new['total_suspicious_indicators'] = df[available_cols].sum(axis=1)
            self.engineered_features.append('total_suspicious_indicators')
        
        # High value access (high volume + high sensitivity)
        if 'data_volume_mb' in df.columns:
            high_volume_threshold = df['data_volume_mb'].quantile(0.9)
            df_new['high_volume_flag'] = (df['data_volume_mb'] > high_volume_threshold).astype(int)
            self.engineered_features.append('high_volume_flag')
        
        return df_new
    
    def engineer_features(self, df):
        """Apply all feature engineering"""
        print("\n" + "=" * 70)
        print("FEATURE ENGINEERING")
        print("=" * 70)
        
        df_engineered = df.copy()
        
        print("\nCreating risk score features...")
        df_engineered = self.create_risk_score_features(df_engineered)
        
        print("Creating interaction features...")
        df_engineered = self.create_interaction_features(df_engineered)
        
        print("Creating temporal features...")
        df_engineered = self.create_temporal_features(df_engineered)
        
        print("Creating anomaly indicators...")
        df_engineered = self.create_anomaly_indicators(df_engineered)
        
        # Note: Aggregation features require user_id which might not be used in training
        # Uncomment if needed
        # print("Creating aggregation features...")
        # df_engineered = self.create_aggregation_features(df_engineered)
        
        print(f"\n✓ Feature engineering completed")
        print(f"✓ New features created: {len(self.engineered_features)}")
        print(f"✓ Total features now: {len(df_engineered.columns)}")
        
        return df_engineered


def main():
    """Test feature engineering module"""
    from config import DATASET_PATH
    
    print("=" * 70)
    print("TESTING FEATURE ENGINEERING MODULE")
    print("=" * 70)
    
    # Load data
    print("\nLoading dataset...")
    df = pd.read_csv(DATASET_PATH)
    print(f"✓ Dataset loaded: {df.shape}")
    
    # Create feature engineer
    engineer = FeatureEngineer()
    
    # Engineer features
    df_engineered = engineer.engineer_features(df)
    
    print("\n" + "=" * 70)
    print("SAMPLE ENGINEERED FEATURES")
    print("=" * 70)
    print(df_engineered[engineer.engineered_features].head())
    
    print("\n" + "=" * 70)
    print("✓ Feature engineering test completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
