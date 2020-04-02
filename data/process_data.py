# import packages
import sys
import pandas as pd
from sqlalchemy import create_engine


def extract_data():
    """
    data extraction from csv files
    """
    messages = pd.read_csv(messages_filename)
    categories = pd.read_csv(categories_filename)
    return messages, categories

def transform_data(messages, categories):
    """
    data clean and transform
    """
    # merge datasets
    df = messages.merge(categories, on='id')
    
    # create a dataframe of the 36 individual category columns
    categories = df.categories.str.split(';', expand=True)
    
    # Rename the column name of categories dataframe
    row = categories.iloc[0,:]
    category_colnames = [x[:-2] for x in row]
    categories.columns = category_colnames
    
    # clean the value of the categories dataframe
    for column in categories:
        categories[column] = categories[column].str[-1:]
        categories[column] = categories[column].astype('int')
    
    # drop the original categories column and concatenate the new `categories`
    df.drop('categories', axis=1, inplace =True)
    df = pd.concat([df, categories],axis = 1)
    
    # drop duplicates
    df.drop_duplicates(inplace=True)
    return df
# 
# 
def load_data(df):
    engine = create_engine('sqlite:///'+database_filename)
    with engine.connect() as con:
        con.execute('drop table if exists disaster')
    df.to_sql('disaster', engine, index=False)
    return
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Error: 4 input arguments needed!')
        exit()
    # get filename of dataset
    _, messages_filename, categories_filename, database_filename = sys.argv
    messages, categories = extract_data()
    df = transform_data(messages, categories)
    load_data(df)
    
    
