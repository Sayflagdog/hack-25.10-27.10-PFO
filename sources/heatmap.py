import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_heatmap(file_path):
    data = pd.read_csv(file_path)

    heatmap_data = data.corr() 

    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Тепловая карта корреляции')
    plt.savefig('resources/heatmap.png') 

