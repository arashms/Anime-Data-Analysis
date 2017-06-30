import seaborn as sns
import pandas as pd
import inspect
import os
import matplotlib.pyplot as plt
import numpy as np
sns.set()
tips = sns.load_dataset("tips")

def ecdf(data):		
    n = len(data)		
    x = np.sort(data)		
    y = np.arange(1, n+1) / n		
    return x, y
 
def initialize_data():

    module_path = inspect.getfile(inspect.currentframe())
    module_dir = os.path.realpath(os.path.dirname(module_path))
    
    data = pd.read_csv(module_dir+"/my_csv2.csv", encoding = "ISO-8859-1")
    data = data.set_index("ID")
    print(list(data.columns.values))
    
    data[['Score','Popularity','ScoredBy']] = data[['Score','Popularity','ScoredBy']].apply(pd.to_numeric,errors='coerce')
    tv_data = data[data["Type"] == "TV"]
    ova_data = data[data["Type"] == "OVA"]
    combined_data = pd.concat([tv_data, ova_data])
    
    non_h_combined_data = combined_data[combined_data["Rating"] != "Rx - Hentai"]
    
    cleaned_data = non_h_combined_data[non_h_combined_data["ScoredBy"] >= 50]
    cleaned_data[["ScoredBy"]] = cleaned_data[["ScoredBy"]].apply(np.log)
    return cleaned_data

def make_histogram(data, variable):
    n_bins = int(np.sqrt(len(data[variable])))
    data = data[variable].dropna()
    plt.hist(data, bins = n_bins)
    plt.show()
    
def make_exp_histogram(data, variable):
    n_bins = int(np.sqrt(len(data[variable])))
    data[[variable]] = data[[variable]].apply(np.exp)
    plt.hist(data[variable].dropna(), bins = n_bins)
    plt.show()
    
def make_ecdf(data, variable):
    x,y = ecdf(data[variable].tolist())
    plt.plot(x,y,marker = ".", linestyle = "none")
    sns.plt.show()
    
def make_exp_ecdf(data, variable):
    data[[variable]] = data[[variable]].apply(np.exp)
    x,y = ecdf(data[variable].tolist())
    plt.plot(x,y,marker = ".", linestyle = "none")
    sns.plt.show()
    
def studio_vs_ratings(non_h_combined_data):
    
    all_studio_data = []
    non_h_combined_data['Std'] = ""
    for studio in (non_h_combined_data.Studios.unique()):
        if ("," not in studio) and (studio != "None found, add some") and ((non_h_combined_data['Studios'] == studio).sum() > 20):
            studio_data = non_h_combined_data[non_h_combined_data['Studios'].str.contains(studio)]
            (studio_data.loc[:,['Std']]) = studio 
            all_studio_data.append(studio_data)
        
    result = pd.concat(all_studio_data)

    ax = sns.boxplot(x="Std", y="Score", data=result)
    plt.xticks(rotation=90)
    plt.tight_layout()
    sns.plt.show()
    
def studio_vs_popularity(non_h_combined_data):
    
    all_studio_data = []
    non_h_combined_data['Std'] = ""
    for studio in (non_h_combined_data.Studios.unique()):
        if ("," not in studio) and (studio != "None found, add some") and ((non_h_combined_data['Studios'] == studio).sum() > 20):
            studio_data = non_h_combined_data[non_h_combined_data['Studios'].str.contains(studio)]
            (studio_data.loc[:,['Std']]) = studio 
            all_studio_data.append(studio_data)
        
    result = pd.concat(all_studio_data)

    ax = sns.boxplot(x="Std", y="ScoredBy", data=result)
    plt.xticks(rotation=90)
    plt.tight_layout()
    sns.plt.show()
    
def source_vs_ratings(non_h_combined_data):
    
    all_source_data = []
    source_means = []
    source_stddev = []
    
    for source in (non_h_combined_data.Source.unique()):
        source_data = non_h_combined_data[non_h_combined_data['Source'] == source] 
        all_source_data.append(source_data)
        source_means.append(round(float(source_data.loc[:,["Score"]].mean()),2))
        source_stddev.append(round(float(source_data.loc[:,["Score"]].std()),2))
    result = pd.concat(all_source_data)
    
    ax = sns.boxplot(x="Source", y="Score", data=result)
    plt.xticks(rotation=45)
    plt.tight_layout()
    sns.plt.show()

def source_vs_popularity(non_h_combined_data):
    
    all_source_data = []
    source_means = []
    source_stddev = []
    
    for source in (non_h_combined_data.Source.unique()):
        source_data = non_h_combined_data[non_h_combined_data['Source'] == source] 
        all_source_data.append(source_data)
        source_means.append(round(float(source_data.loc[:,["ScoredBy"]].mean()),2))
        source_stddev.append(round(float(source_data.loc[:,["ScoredBy"]].std()),2))
    result = pd.concat(all_source_data)
    
    ax = sns.boxplot(x="Source", y="ScoredBy", data=result)
    print(source_means)
    print(source_stddev)
    plt.xticks(rotation=45)
    plt.tight_layout()
    sns.plt.show()
    
def genre_vs_ratings(non_h_combined_data):
    temp = non_h_combined_data
    non_h_combined_data = non_h_combined_data.astype('object')
    for i in non_h_combined_data.index.values.tolist():
        a = [x.strip() for x in non_h_combined_data.loc[i]["Genres"].split(',')]
        non_h_combined_data["Genres"][i] = a
    
    unique_genres = []
    count = 0
    for genre_list in non_h_combined_data["Genres"]:
        for j in range(len(genre_list)):
                if genre_list[j] not in unique_genres:
                        unique_genres.append(genre_list[j])
        
        count += 1

    unique_genres.remove('No genres have been added y')
    print(unique_genres)
    
    non_h_combined_data = temp
    non_h_combined_data['Genre'] = ""
    all_genre_data = []
    for genre in (unique_genres):
        genre_data = non_h_combined_data[non_h_combined_data['Genres'].str.contains(genre)]
        (non_h_combined_data.head())
        genre_data.loc[:,['Genre']] = genre
        all_genre_data.append(genre_data)
    result = pd.concat(all_genre_data)
    
    ax = sns.boxplot(x="Genre", y="Score", data=result)
    plt.xticks(rotation=90)
    plt.tight_layout()
    sns.plt.show()
    
def genre_vs_popularity(non_h_combined_data):
    temp = non_h_combined_data
    non_h_combined_data = non_h_combined_data.astype('object')
    for i in non_h_combined_data.index.values.tolist():
        a = [x.strip() for x in non_h_combined_data.loc[i]["Genres"].split(',')]
        non_h_combined_data["Genres"][i] = a
    
    unique_genres = []
    count = 0
    for genre_list in non_h_combined_data["Genres"]:
        for j in range(len(genre_list)):
                if genre_list[j] not in unique_genres:
                        unique_genres.append(genre_list[j])
        
        count += 1

    unique_genres.remove('No genres have been added y')

    non_h_combined_data = temp
    non_h_combined_data['Genre'] = ""
    all_genre_data = []
    for genre in (unique_genres):
        genre_data = non_h_combined_data[non_h_combined_data['Genres'].str.contains(genre)]
        (non_h_combined_data.head())
        genre_data.loc[:,['Genre']] = genre
        all_genre_data.append(genre_data)
    result = pd.concat(all_genre_data)
    
    ax = sns.boxplot(x="Genre", y="ScoredBy", data=result)
    plt.xticks(rotation=90)
    plt.tight_layout()
    sns.plt.show()
#def make histogram of ratings

#def make histogram of popularity



def testing(non_h_combined_data):
    #print((non_h_combined_data.Source.value_counts()))
    return
    
if __name__ == "__main__":
    data = initialize_data()
    
    #studio_vs_popularity(data)
    #studio_vs_ratings(data)
    
    #source_vs_popularity(data)
    #source_vs_ratings(data)
    
    #genre_vs_ratings(data)
    #genre_vs_popularity(data)
    
    #make_ecdf(data, "Score")
    #make_ecdf(data, "ScoredBy")
    #make_exp_ecdf(data, "ScoredBy")
    
    #make_histogram(data, "Score")
    #make_histogram(data, "ScoredBy")
    make_exp_histogram(data, "ScoredBy")
    testing(data)
    