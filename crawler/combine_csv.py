import pandas as pd

def df_to_list(df):
    return df.drop(index=0).drop(columns=[0.0]).values.tolist()


if __name__ == "__main__":
    file_path_1 = "/Users/lc2002/Documents/2022-1/homework/DataWarehouse/crawler/movies-info/movies-0w-15w.csv"
    file_path_2 = "/Users/lc2002/Documents/2022-1/homework/DataWarehouse/crawler/movies-info/movies-15w-24w.csv"
    output_file_path = "/Users/lc2002/Documents/2022-1/homework/DataWarehouse/crawler/movies-info/movies-0w-24w.csv"
    file_1 = pd.read_csv(file_path_1, header=None)
    file_2 = pd.read_csv(file_path_2, header=None)
    list_1 = df_to_list(file_1)
    list_2 = df_to_list(file_2)
    list_1.extend(list_2)
    name = ["asin", "title", "genre", "release_data", "first_available_date", "actor", "director", "format", "run_time", "language"]
    csv_file = pd.DataFrame(columns=name, data=list_1)
    csv_file.to_csv(output_file_path)
    