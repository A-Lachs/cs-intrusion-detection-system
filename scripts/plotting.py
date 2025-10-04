# collection of functions used for plotting 
import pandas as pd 

# custom colors for palette
COLOR_1 = 'steelblue'
COLOR_2 =  '#E42A38'

def aggregate_feature_by_target(data_df: pd.DataFrame, feature: str, target, verbose=1) -> pd.DataFrame:
    """ This function takes a categorical feature of from data_df and counts it grouped by the target variable.
        It also returns a df with the percentages.

    Args:
        data_df (pd.DataFrame): df that contains feature and target var for each client
        feature (str):          name of feature to aggregate
        target (str, optional): name of target variable to group by. Defaults to 'target'.

    Returns:
        pd.DataFrame: grouped df
    """
    if target:
        grouped_object = data_df.groupby(feature, observed=False, as_index=False, dropna=False)[target]
         # calculate count and proportion
        df_count = grouped_object.value_counts(dropna=False) 
        df_proportion = grouped_object.value_counts(dropna=False, normalize=True)
        # merge count and proportion 
        aggregated_df = df_count.merge(df_proportion, how='inner', on=[feature, target]) 
        aggregated_df.sort_values([target, 'proportion'], ascending=False, inplace=True)
    else:
         # calculate count and proportion
        df_count = data_df[feature].value_counts(dropna=False).reset_index()
        df_proportion = data_df[feature].value_counts(dropna=False, normalize=True).reset_index()
        # merge count and proportion 
        aggregated_df = df_count.merge(df_proportion, how='inner', on=[feature])
        aggregated_df.sort_values(['proportion'], ascending=False, inplace=True)
        
    #  converting to percent
    aggregated_df['proportion']= aggregated_df['proportion']*100
    aggregated_df.rename({'proportion': 'percent'}, axis=1, inplace=True)

    # print statements about the relative percentage the target was 1 for each category
    if verbose:
        # total count 
        tc = data_df[feature].value_counts(dropna=False).reset_index()

        for feature_category in aggregated_df[feature].unique():
            abs_freq = tc[tc[feature] == feature_category]["count"].values[0]
            rel_percent = aggregated_df[(aggregated_df[feature] == feature_category ) & (aggregated_df[target] == 1)].percent.values[0]
            print(f"For {feature} { feature_category} {round(rel_percent,2)}% of traffic was an attack (based on {abs_freq} data points).")

    return aggregated_df
