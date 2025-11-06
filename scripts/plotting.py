##########################################################
### Collection of functions used for eda and plotting  ###
##########################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------- define default parameters ----------------------------------
# custom colors for palette
COLOR_1 = 'steelblue'
COLOR_2 =  '#E42A38'

TARGET_LABELS = ["genuine", "malicious"]

# headline parameters
TITLE_STYLES = {
    "main": {"fontsize": 12, "fontweight": "bold", "y": 0.92},
    "sub": {"fontsize": 10, "fontweight": "normal", 'loc':'left', 'pad': 8},}


#  --------------------------------------- helper functions -----------------------------------------

def pretty_category_str(feature:str) -> str:
    """Returns a pretty string of input feature, capitalized and in plural.
       Used for plot titles.
    """
    category_name = feature.replace("_", " ").capitalize()
    if category_name.endswith("y"):
        category_name = category_name[:-1] + "ie"
    return category_name + "s"


def adjust_title_styles(n_categories: int):
    """
    Returns adjusted title styles and layout depending on number of categories.
    Keeps TITLE_STYLES unchanged.
    Usage: When horizontal barplot height is dynamically adjusted with nr of categories, 
    title parameters (y and pad) and layout need to be adapted, too.

        - y     -> vertical pos of title relative to fig: 0 bottom of fig, 1 top of fig
        - pad   -> vertical space in point between title txt and axes
        - top_margin -> in plt.tight_layout(rect=[0, 0, 1, top_margin]) is increased
          to leave enough space at top of fig (for titles)
    """
    styles = TITLE_STYLES

    # smooth scaling factor between 0 (compact) and 1 (spacious)
    scale = np.clip((n_categories - 10) / 60, 0, 1)

    # adjust figure title position (slightly higher for tall plots)
    styles["main"]["y"] = 0.92 + 0.03 * scale

    # adjust subtitle padding (less space when tall)
    styles["sub"]["pad"] = 10 - 7 * scale
    
    # adjust layout rect top margin (space reserved for titles)
    top_margin =  0.95 + 0.02 * scale
    layout_rect = [0, 0, 1, top_margin]

    return styles, layout_rect

# -------------------------------------------- pie plot ---------------------------------------------

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
    category_name = pretty_category_str(feature)
    # to center title use figure title (not axis title) 
    fig.suptitle(f"Different {category_name} in training data", **TITLE_STYLES['main'])

    # equal aspect ratio ensures pie is drawn as circle
    ax.axis("equal")

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # leave 5% of top figure height free (for titles)
    plt.show()

# ---------------------------------------------- bar plots --------------------------------------------

def barplot_frequency_by_attack(data_df: pd.DataFrame, feature:str, target:str):
    """
    Horizontal bar plot, plot frequency of network traffic grouped by target (genuine vs malicious) 
    and a categorical feature.
    The data_df has count and percent of the feature categories grouped by target.
    
    Note: 
    Use the helper function aggregate_feature_by_categories() to create this data_df, 
    it also makes sure that the categories are ranked by percent of malicious network traffic descending.
    
    Features: 
    - y-tick labels include the percentage of malicious network traffic for each category.
    - Plot hight is increased with nr of catogories of inut feature.
    
    Args:
        data_df (pd.DataFrame): DF with count and percent of the feature categories grouped by target.
        feature (str):          Name of categorical feature
        target (str):           Name of (binary) target feature
    """
    
    category_oder = data_df[feature].unique()   # keep category order of the input df for plotting
    n_categories = len(category_oder)
    
    plot_width = 6
    plot_height = 4

    # adjust plot height by nr of categories 
    plot_height = max(plot_height, n_categories* 0.2)

    plt.figure(figsize=(plot_width, plot_height))  
    
    # plot data 
    ax = sns.barplot(
        data=data_df, 
        x="count", 
        y=feature, 
        hue=target, 
        order=category_oder,        # keep feature order of the input df
        palette=[COLOR_1, COLOR_2]
        )

    # load and adapt default title styles relative to nr of categories
    styles, layout_rect = adjust_title_styles(n_categories)

    # optimize figure title 
    renamed_feature = pretty_category_str(feature)
    plt.suptitle(f"Frequency of network traffic by {renamed_feature}",
                  **styles["main"])
    # add subtitle 
    plt.title("Ranked by malicious traffic percentage (%)", 
              **styles["sub"])

    # optimize legend title and labels
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, TARGET_LABELS, title="")

    # optimize y and x labels
    ax.set_ylabel(feature.replace("_", " ").capitalize())
    ax.set_xlabel("Number of cases")

    # --- modify y-tick labels (add % of attacks to each category)

    # set y-ticks 
    ax.set_yticks(range(len(category_oder))) # fixed pos for each category
    
    # get a series with % attacks for each category
    percent_attack =  (   
        data_df.loc[data_df[target] == 1, [feature, "percent"]]
        .set_index(feature)["percent"]
        .round(0)  # round to whole numbers
        .astype(int))
    
    # create new labels 
    new_labels = [
        f"{str(cat).capitalize()} ({percent_attack.get(cat, 0)}%)"
        for cat in category_oder]
    
    # set y-tick labels 
    ax.set_yticklabels(new_labels, va='center')
    
    plt.tight_layout(rect=layout_rect) # leave space at top of figure (for titles)
    plt.show()


def barplot_percent_by_attack(data_df:pd.DataFrame, sub_df:pd.DataFrame, feature:str, target:str):
    """
    Horizontal bar plot, plot percent of malicious network traffic by feature.
    The data_df has count and percent of the feature categories grouped by target.
    The sub_df has count and percent of the feature categories grouped where target == 1 (malicious network traffic)
    - Optional: The sub df can be further subset (e.g by percent) to plot only a portion of the data
                (Useful when the feature has many categories). 
    
    Note:
    Use the helper function aggregate_feature_by_categories() to create this data_df, 
    it also makes sure that the categories are ranked by percent of malicious network traffic descending.
    
    Features:
    - y-tick labels include the number of total cases for each category.
    - Plot hight is increased with nr of catogories of inut feature. 
    
    Args:
        data_df (pd.DataFrame): DF with count and percent of the feature categories grouped by target.
        sub_df (pd.DataFrame):  part of data_df, expect: where target == 1 
        feature (str):          Name of categorical feature
        target (str):           Name of (binary) target feature
    """

    category_oder = sub_df[feature].unique() # keep category order of the sub df for plotting
    n_categories = len(category_oder)
    
    plot_width = 6
    plot_height = 4

    # adjust plot height by nr of categories 
    plot_height = max(plot_height, n_categories* 0.2)

    plt.figure(figsize=(plot_width, plot_height))    

    # seaborn barblot
    ax = sns.barplot(
            data=sub_df, 
            x="percent", 
            y=feature,
            order=category_oder, # keep feature order of the input df
            color=COLOR_2,       # only red for malicious network traffic
    )

    # load and adapt default title styles relative to nr of categories
    styles, layout_rect = adjust_title_styles(n_categories)

    # optimize legend
    ax.legend_ = None

    # optimize figure title 
    renamed_feature = pretty_category_str(feature)
    plt.suptitle(f"Percent of malicious network traffic by {renamed_feature}",
                  ** styles['main'])
    # add subtitle 
    plt.title("Ranked by percentage descending (n total cases)",
               **styles['sub'])
    
    # optimize y and x labels
    ax.set_ylabel(feature.replace("_", " ").capitalize())
    ax.set_xlabel("Percent")
    ax.set_xlim(0, 100)

    # --- modify y-tick labels (add n of total cases to each category)

    # set y-ticks 
    ax.set_yticks(range(len(category_oder))) # fixed pos for each category
    
    # Compute total counts per category (sum over both attack=0 and attack=1) 
    total_counts = (
        data_df.groupby(feature, observed=False)['count']
        .sum()
        .reindex(sub_df[feature].values)  # keep same order as plotted data
    )
    # create new labels 
    new_labels = [
        f"{str(cat).capitalize()} (n={total_counts.get(cat, 0)})"
        for cat in category_oder]
    
    # set y-tick labels 
    ax.set_yticklabels(new_labels, va='center')

    plt.tight_layout(rect=layout_rect)  # leave space at top of figure (for titles)
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
    

def aggregate_feature_by_categories(data_df: pd.DataFrame, feature: str, target:str, verbose=1) -> pd.DataFrame:
    """ 
    This function takes a categorical variable (= feature) of from data_df and returns a df with the count 
    and percent for each category of the feature. 
    - Optional:  If target variable is defined, additionally group the feature by a target variable.
    - Optional:  If verbose, add a print statement.   
    
    Args:
        data_df (pd.DataFrame): df that contains feature (and target) variable.
        feature (str):          Name of categorical variable used to aggregate.
        target (str, optional): Name of categorical target variable to group by.

    Returns:
        pd.DataFrame: aggregated df with columns: feature, (target), count and percent.
    """
    # additionally group by trarget
    if target:
        grouped_object = data_df.groupby(feature, observed=False, as_index=False, dropna=False)[target]
         # calculate count and proportion
        df_count = grouped_object.value_counts(dropna=False) 
        df_proportion = grouped_object.value_counts(dropna=False, normalize=True)
        # merge count and proportion 
        aggregated_df = df_count.merge(df_proportion, how='inner', on=[feature, target]) 
        aggregated_df.sort_values([target, 'proportion'], ascending=False, inplace=True)
    
    # aggregate by feature categories
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

    # Optional print statements
    # for each feature category print the percent of target = 1  and total freq of that category 
    if verbose and target:
        # total count 
        tc = data_df[feature].value_counts(dropna=False).reset_index()
        print(f"--- Feature categories of '{feature}':")
        for feature_category in aggregated_df[feature].unique():
            total_freq = tc[tc[feature] == feature_category]["count"].values[0]
            rel_percent = aggregated_df[(aggregated_df[feature] == feature_category ) & (aggregated_df[target] == 1)].percent.values[0]
            print(f"For {feature_category} {round(rel_percent,2)}% of network traffic was an attack (of {total_freq} total cases).")

    return aggregated_df


