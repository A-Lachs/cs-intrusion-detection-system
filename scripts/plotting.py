##########################################################
### Collection of functions used for eda and plotting  ###
##########################################################

import pandas as pd
import matplotlib.pyplot as plt

# custom colors for palette
COLOR_1 = 'steelblue'
COLOR_2 =  '#E42A38'

# --------------------------------------- pie plot --------------------------------------------

def plot_to_pie(data_df, feature):
    """
    Creates a pie chart of the feature variable.
    Accepts either raw data (one row per observation) or a dataframe with proportions.
    """

    # if proportions are not provided, compute them
    if "proportion" not in data_df.columns:
        df_proportions= (
            data_df[feature]
            .value_counts(normalize=True)
            .rename_axis(feature)
            .reset_index(name="proportion")
        )
    else:
        df_proportions = data_df.copy()

    # shift large pie slices slightly outwards
    explode = [0.04 if p > 0.1 else 0 for p in df_proportions["proportion"]]

    # create figure and axes
    fig, ax = plt.subplots(figsize=(5, 5))

    # pie plot
    wedges, texts, autotexts = ax.pie(
        df_proportions["proportion"],
        labels=df_proportions[feature],
        autopct="%1.0f%%",      # format and display percentages
        explode=explode,
        pctdistance=0.85,       # move percentages outward
        labeldistance=1.10,     # move labels outward
        startangle=30,          # makes the pie start at top for consistency
        textprops={"fontsize": 11},
    )

    # optimize title 
    category_name = feature.replace("_", " ").capitalize()
    if category_name.endswith("y"):
        category_name = category_name[:-1] + "ie"
    
    # center title: use figure title (not axis title) for better centering
    fig.suptitle(f"Different {category_name}s in training data\n",
                 fontsize=14, fontweight="normal", y=0.92)

    # equal aspect ratio ensures pie is drawn as circle
    ax.axis("equal")

    plt.tight_layout()
    plt.show()


# --------------------------------------- aggregation functions ---------------------------------------

def sum_category_by_proportion(data_df:pd.DataFrame, 
                               feature:str, 
                               new_category="other", 
                               threshold=0.02) -> pd.DataFrame | None:

    """ 
    Calculate the proportions of a categorical feature from a data_df and 
    summarize categories with proportions smaller than the threshold value to a new_category.
    Usage: Strategy used to reduce nr of catetogories to plot categorical features nicely. 
    
    Returns:
    - None if the new_category name already exists.
    - None it the feature is not of datatype category. 
    - Otherwise, return a df with sorted proportions of the feature categories, with a new_category 
    that summarizes all categories with proportions < threshold.
    """
    
 
    # get df with proportions for feature variable categories 
    df_prop = data_df[feature].value_counts(normalize=True).reset_index()

    # check if feature is categorical 
    if isinstance(df_prop[feature].dtype, pd.CategoricalDtype):
        # check if new category already exists
        if  new_category not in df_prop[feature].cat.categories:
            df_prop[feature] = df_prop[feature].cat.add_categories([new_category])
        else:
            print(f"Category {new_category} already exists.")
            return

        # assign new_category based on threshold
        df_prop.loc[df_prop.proportion < threshold, feature] = new_category
        # sum up values of new category and sort values for plotting
        df_reduced_cat = df_prop.groupby(feature, observed=True, as_index=False).proportion.sum()
        df_reduced_cat.sort_values("proportion", ascending=False, inplace=True)

        return df_reduced_cat

    else:
        print(f"The feature {feature} is not categorical.")
        return
    
    
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


