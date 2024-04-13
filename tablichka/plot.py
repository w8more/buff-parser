import asyncio
import matplotlib.pyplot as plt
import pandas as pd
from parse import get_df


def plot_quantities(display_type):
    df = asyncio.run(get_df("capsule_quantites"))
    y_columns = [
        "paris_2023_legends_sticker_capsule", "paris_2023_contenders_sticker_capsule", "paris_2023_challengers_sticker_capsule",
        "antwerp_2022_challengers_sticker_capsule", "antwerp_2022_legends_sticker_capsule", "antwerp_2022_contenders_sticker_capsule", 
        "rmr_2020_contenders", "rmr_2020_challengers", "rmr_2020_legends", 
        "sticker__9ine__paris_2023"
    ]
    x = df.date
    y = df.loc[:, y_columns]

    plt.figure(figsize=(20,12), dpi=100)

    if display_type == "paris" or display_type == "all":
        plt.plot(x,df[y_columns[0]],label=y_columns[0],color='green', marker='o',linestyle='dashed',linewidth=2,markersize=12)
        plt.plot(x,df[y_columns[1]],label=y_columns[1],color='red', marker='o',linestyle='dashed',linewidth=2,markersize=12)
        plt.plot(x,df[y_columns[2]],label=y_columns[2],color='yellow', marker='o',linestyle='dashed',linewidth=2,markersize=12)
    if display_type == "antwerp" or display_type == "all":
        plt.plot(x,df[y_columns[3]],label=y_columns[3],color='orange', marker='o',linestyle='dashed',linewidth=2,markersize=12)
        plt.plot(x,df[y_columns[4]],label=y_columns[4],color='blue', marker='o',linestyle='dashed',linewidth=2,markersize=12)
        plt.plot(x,df[y_columns[5]],label=y_columns[5],color='black', marker='o',linestyle='dashed',linewidth=2,markersize=12)
    if display_type == "rmr" or display_type == "all":
        plt.plot(x,df[y_columns[6]],label=y_columns[6],color='cyan', marker='o',linestyle='dashed',linewidth=2,markersize=12)
        plt.plot(x,df[y_columns[7]],label=y_columns[7],color='brown', marker='o',linestyle='dashed',linewidth=2,markersize=12)
        plt.plot(x,df[y_columns[8]],label=y_columns[8],color='magenta', marker='o',linestyle='dashed',linewidth=2,markersize=12)
    if display_type == "9ine" or display_type == "all":
        plt.plot(x,df[y_columns[9]],label=y_columns[9],color='olive', marker='o',linestyle='dashed',linewidth=2,markersize=12)

    plt.title("Quantity of capsules", fontdict={'fontname': 'Comic Sans MS', 'fontsize': 20})
    plt.xlabel("date", fontdict={"fontname" : "monospace", 'fontsize': 14})
    plt.ylabel("capsules", fontdict={"fontname" : "monospace", 'fontsize': 14})
    plt.legend()
    plt.show()

def test():
    df = asyncio.run(get_df("capsule_quantites"))
    y_columns = [
        "paris_2023_legends_sticker_capsule", "paris_2023_contenders_sticker_capsule", "paris_2023_challengers_sticker_capsule"
    ]

    df['date'] = pd.to_datetime(df['date'])
    weekly_means = df.resample('W-Mon', on='date').mean()

    x = df.date
    y = df.loc[:, y_columns]



    plt.figure(figsize=(20,12), dpi=100)

    plt.plot(x,df[y_columns[0]],label=y_columns[0],color='green', marker='o',linestyle='dashed',linewidth=2,markersize=12)
    plt.plot(x,df[y_columns[1]],label=y_columns[1],color='red', marker='o',linestyle='dashed',linewidth=2,markersize=12)
    plt.plot(x,df[y_columns[2]],label=y_columns[2],color='yellow', marker='o',linestyle='dashed',linewidth=2,markersize=12)

    plt.legend()
    plt.show()


def main():
    capsule_types = ["paris","antwerp", "rmr", "9ine"]
    # plot_quantities("paris")
    test()

if __name__ == "__main__":
    main()