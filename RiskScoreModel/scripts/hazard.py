import pandas as pd
import numpy as np
from tqdm import tqdm 
import os
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

def calculate_hazard_scores(df, hazard_vars):
    """
    Calculate hazard scores using a single classification step.
    
    Args:
        df: DataFrame containing hazard variables
        hazard_vars: List of column names for hazard variables
        
    Returns:
        DataFrame with flood hazard classifications
    """
    # Log transform and standardize variables
    transformed_data = pd.DataFrame()
    for var in hazard_vars:
        transformed_data[var] = np.log1p(df[var])
        transformed_data[var] = (transformed_data[var] - transformed_data[var].mean()) / transformed_data[var].std()
    
    # Calculate composite score
    df['flood-hazard-float'] = transformed_data[hazard_vars].mean(axis=1)
    
    # Apply final classification
    thresholds = [
        df['flood-hazard-float'].quantile(0.35),
        df['flood-hazard-float'].quantile(0.60),
        df['flood-hazard-float'].quantile(0.80),
        df['flood-hazard-float'].quantile(0.95)
    ]
    
    conditions = [df['flood-hazard-float'] <= thresholds[0]]
    for i in range(len(thresholds) - 1):
        conditions.append(
            (df['flood-hazard-float'] > thresholds[i]) & 
            (df['flood-hazard-float'] <= thresholds[i + 1])
        )
    conditions.append(df['flood-hazard-float'] > thresholds[-1])
    
    df['flood-hazard'] = np.select(conditions, [1, 2, 3, 4, 5], default=1)
    
    return df[['timeperiod', 'object_id', 'flood-hazard', 'flood-hazard-float']]

def plot_hazard_distribution(df, output_path=None):
    """
    Create visualizations of the hazard distribution.
    
    Args:
        df: DataFrame containing hazard classifications
        output_path: Optional path to save the plots
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar plot
    sns.countplot(data=df, x='flood-hazard', ax=ax1, color='steelblue')
    ax1.set_title('Distribution of Flood Hazard Classes', pad=15)
    ax1.set_xlabel('Hazard Class')
    ax1.set_ylabel('Count')
    
    # Add count labels
    for p in ax1.patches:
        ax1.annotate(f'{int(p.get_height()):,}', 
                    (p.get_x() + p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=10)
    
    # Box plot
    sns.boxplot(data=df, x='flood-hazard', y='flood-hazard-float', ax=ax2, color='lightblue')
    ax2.set_title('Distribution of Float Values by Hazard Class', pad=15)
    ax2.set_xlabel('Hazard Class')
    ax2.set_ylabel('Standardized Hazard Score')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved to: {output_path}")
    
    plt.show()

def validate_hazard_distribution(df):
    """
    Validate the hazard distribution and print statistics.
    
    Args:
        df: DataFrame containing hazard classifications
        
    Returns:
        bool: True if all validation checks pass
    """
    dist = df['flood-hazard'].value_counts().sort_index()
    total = len(df)
    
    print("\nHazard Distribution Validation:")
    print("-" * 40)
    
    for class_num in range(1, 6):
        count = dist.get(class_num, 0)
        percentage = (count / total) * 100
        print(f"Class {class_num}: {count:,} ({percentage:.1f}%)")
    
    checks = {
        "All classes present": len(dist) == 5,
        "Class range valid": df['flood-hazard'].between(1, 5).all(),
        "Decreasing trend": dist.iloc[0] > dist.iloc[-1],
        "No missing values": df['flood-hazard'].notna().all()
    }
    
    print("\nValidation Checks:")
    print("-" * 40)
    for check, result in checks.items():
        print(f"{check}: {'✓' if result else '✗'}")
    
    return all(checks.values())

def print_variable_statistics(df, hazard_vars):
    """
    Print summary statistics for each hazard variable.
    
    Args:
        df: DataFrame containing hazard variables
        hazard_vars: List of column names for hazard variables
    """
    print("\nVariable Statistics:")
    print("-" * 40)
    
    for var in hazard_vars:
        stats = df[var].describe()
        print(f"\n{var}:")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Std: {stats['std']:.2f}")
        print(f"  Min: {stats['min']:.2f}")
        print(f"  Max: {stats['max']:.2f}")
        print(f"  Skew: {df[var].skew():.2f}")

def main():
    # Configuration
    hazard_vars = [
        'inundation_intensity_mean_nonzero', 
        'inundation_intensity_sum',
        'drainage_density', 
        'mean_rain', 
        'max_rain'
    ]
    
    # Read data
    base_path = os.path.join(os.getcwd(), 'RiskScoreModel', 'data')
    master_variables = pd.read_csv(os.path.join(base_path, 'MASTER_VARIABLES.csv'))
    
    # Print initial statistics
    print_variable_statistics(master_variables, hazard_vars)
    
    # Process each time period
    results = []
    for month in tqdm(master_variables['timeperiod'].unique()):
        month_data = master_variables[
            master_variables['timeperiod'] == month
        ][hazard_vars + ['timeperiod', 'object_id']].copy()
        
        results.append(calculate_hazard_scores(month_data, hazard_vars))
    
    # Combine and merge results
    hazard_scores = pd.concat(results)
    master_variables = master_variables.merge(
        hazard_scores, 
        on=['timeperiod', 'object_id']
    )
    
    # Validate and visualize
    is_valid = validate_hazard_distribution(master_variables)
    if is_valid:
        print("\nHazard distribution passes all validation checks!")
    else:
        print("\nWarning: Some validation checks failed. Please review the distribution.")
    
    plot_hazard_distribution(
        master_variables,
        os.path.join(base_path, 'hazard_distribution.png')
    )
    
    # Save results
    master_variables.to_csv(
        os.path.join(base_path, 'factor_scores_l1_flood-hazard.csv'),
        index=False
    )
    print(f"\nResults saved successfully!")

if __name__ == "__main__":
    main()