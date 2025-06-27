import pandas as pd
import numpy as np
from tqdm import tqdm 
import os
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress all warnings
warnings.filterwarnings("ignore")

def plot_hazard_distribution(df, output_path=None):
    """
    Create visualizations of the hazard distribution.
    
    Args:
        df: DataFrame containing hazard classifications
        output_path: Optional path to save the plots
    """
    # Set up the plotting style
    plt.style.use('default')  # Using default matplotlib style instead of seaborn
    
    # Create figure and subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Bar plot of hazard distribution
    sns.countplot(data=df, x='flood-hazard', ax=ax1, color='steelblue')
    ax1.set_title('Distribution of Flood Hazard Classes', pad=15)
    ax1.set_xlabel('Hazard Class')
    ax1.set_ylabel('Count')
    
    # Add count labels on top of bars
    for p in ax1.patches:
        ax1.annotate(f'{int(p.get_height()):,}', 
                    (p.get_x() + p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=10)
    
    # Plot 2: Box plot of float values by class
    sns.boxplot(data=df, x='flood-hazard', y='flood-hazard-float', ax=ax2, color='lightblue')
    ax2.set_title('Distribution of Float Values by Hazard Class', pad=15)
    ax2.set_xlabel('Hazard Class')
    ax2.set_ylabel('Float Value')
    
    # Adjust layout
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved to: {output_path}")
    
    plt.show()

def validate_hazard_distribution(df, column='flood-hazard'):
    """
    Validate the hazard distribution and print statistics.
    
    Args:
        df: DataFrame containing hazard classifications
        column: Name of the hazard column to validate
    """
    # Calculate distribution
    dist = df[column].value_counts().sort_index()
    total = len(df)
    
    print("\nHazard Distribution Validation:")
    print("-" * 40)
    
    # Print distribution statistics
    for class_num in range(1, 6):
        count = dist.get(class_num, 0)
        percentage = (count / total) * 100
        print(f"Class {class_num}: {count:,} ({percentage:.1f}%)")
    
    # Validation checks
    checks = {
        "All classes present": len(dist) == 5,
        "Class range valid": df[column].between(1, 5).all(),
        "Decreasing trend": dist.iloc[0] > dist.iloc[-1],
        "No missing values": df[column].notna().all()
    }
    
    print("\nValidation Checks:")
    print("-" * 40)
    for check, result in checks.items():
        print(f"{check}: {'✓' if result else '✗'}")
    
    return all(checks.values())

def categorize_column_percentile(df, column_name):
    """
    Categorize values using custom percentile thresholds to ensure a decreasing distribution
    while maintaining representation across all classes.
    """
    values = np.log1p(df[column_name])
    
    thresholds = [
        np.percentile(values, 50),  # median
        np.percentile(values, 75),
        np.percentile(values, 90),
        np.percentile(values, 98)
    ]
    
    conditions = [
        (values <= thresholds[0]),
        (values > thresholds[0]) & (values <= thresholds[1]),
        (values > thresholds[1]) & (values <= thresholds[2]),
        (values > thresholds[2]) & (values <= thresholds[3]),
        (values > thresholds[3])
    ]
    
    categories = [1, 2, 3, 4, 5]
    
    return np.select(conditions, categories, default=1)
def adjust_hazard_classification(float_scores):
    """
    Adjust hazard classification using custom thresholds to ensure more balanced distribution
    
    Args:
        float_scores: Series containing float hazard scores
    
    Returns:
        Series with adjusted integer classifications
    """
    # Define custom thresholds for classification
    thresholds = [
        float_scores.quantile(0.35),  # Class 1 upper bound
        float_scores.quantile(0.60),  # Class 2 upper bound
        float_scores.quantile(0.80),  # Class 3 upper bound
        float_scores.quantile(0.95),  # Class 4 upper bound
    ]
    
    # Create classification based on thresholds
    conditions = [
        (float_scores <= thresholds[0]),
        (float_scores > thresholds[0]) & (float_scores <= thresholds[1]),
        (float_scores > thresholds[1]) & (float_scores <= thresholds[2]),
        (float_scores > thresholds[2]) & (float_scores <= thresholds[3]),
        (float_scores > thresholds[3])
    ]
    
    categories = [1, 2, 3, 4, 5]
    
    return np.select(conditions, categories, default=1)

# Modify the main processing loop
def main():
    # Read the data
    master_variables = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/MASTER_VARIABLES.csv')
    hazard_vars = ['inundation_intensity_mean_nonzero', 'inundation_intensity_sum', 
                   'drainage_density', 'mean_rain', 'max_rain']
    hazard_df = master_variables[hazard_vars + ['timeperiod', 'object_id']]

    hazard_df_months = []
    for month in tqdm(hazard_df.timeperiod.unique()):
        hazard_df_month = hazard_df[hazard_df.timeperiod == month].copy()
        
        # Apply percentile-based categorization to each variable
        for var in hazard_vars:
            hazard_df_month[f'{var}_level'] = categorize_column_percentile(hazard_df_month, var)
        
        # Calculate hazard scores
        level_columns = [f'{var}_level' for var in hazard_vars]
        
        # Calculate average (float) hazard score
        hazard_df_month['flood-hazard-float'] = hazard_df_month[level_columns].mean(axis=1)
        
        # Use custom classification instead of simple rounding
        hazard_df_month['flood-hazard'] = adjust_hazard_classification(
            hazard_df_month['flood-hazard-float']
        )
        
        hazard_df_months.append(hazard_df_month)

    # Combine results
    hazard = pd.concat(hazard_df_months)

    # Merge back to master variables
    master_variables = master_variables.merge(
        hazard[['timeperiod', 'object_id', 'flood-hazard', 'flood-hazard-float']],
        on=['timeperiod', 'object_id']
    )
    
    # Validate the distribution
    is_valid = validate_hazard_distribution(master_variables)
    
    if is_valid:
        print("\nHazard distribution passes all validation checks!")
    else:
        print("\nWarning: Some validation checks failed. Please review the distribution.")
    
    # Create and save visualization
    plot_path = os.path.join(os.getcwd(), 'RiskScoreModel/data/hazard_distribution.png')
    plot_hazard_distribution(master_variables, plot_path)
    
    # Save results
    output_path = os.path.join(os.getcwd(), 'RiskScoreModel/data/factor_scores_l1_flood-hazard.csv')
    master_variables.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()