import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
   "polarity" : [1, 0, -1, 0, 1, -1, 1, 0, -1, 1],
   "PR_state" : [-1, -1, 0, -1, -1, 0, -1, -1, -1, -1],
   "days_since_creation/until_closure" : [10, 549, 2007, 574, 1, 3839, 37, 1106, 2038, 1091],
   "lines_added" : [6, 35, 494, 16, 19, 896, 83, 103, 62, 25],
   "lines_removed" : [2, 0, 0, 1, 0, 0, 41, 1, 9, 0],
   "nb_modified_files" : [2, 2, 2, 1, 1, 4, 1, 2, 2, 2],
   "c_cyclo_diff" : [0, 6, 6, 3, 3, 27, -6, 9, 5, 2],
   "warnings_diff" : [0, 0, 2, 0, 0, 1, 0, 0, 0, 0] 
}

def normalize_df(df) :
    scaled = df.copy()

    for column in scaled.columns:
        if column not in ["polarity", "PR_state"] :
            scaled[column] = (scaled[column] - scaled[column].min()) / (scaled[column].max() - scaled[column].min())

    return scaled

if __name__ == '__main__' :
    df_prelim = pd.DataFrame(data)
    scaled = normalize_df(df_prelim)
    matrix = scaled.corr(method='spearman')

    plt.figure(figsize=(10,8))
    sns.heatmap(matrix, annot=True, cmap="coolwarm_r", fmt=".2f", linewidths=0.5, annot_kws={"size": 14})  
    plt.title("Heatmap de corrélation de l'analyse préliminaire")
    plt.xticks(rotation=45, fontsize=14)  # taille des labels x
    plt.yticks(fontsize=14)     

    plt.show()