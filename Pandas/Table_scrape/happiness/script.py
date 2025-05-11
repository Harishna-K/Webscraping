import pandas as pd  # for data manipulation
import matplotlib.pyplot as plt  # for plotting

url = 'https://en.wikipedia.org/wiki/World_Happiness_Report'
tables = pd.read_html(url)

happiness_table = tables[21]   # 21 is the index of the table we want to scrape

# print("columns names:", happiness_table.columns)  # print the column names of the table

# # happiness_table.columns = ['Rank', 'Country', 'Score']   # rename the columns

# tidy_happiness_table = happiness_table.iloc[:].copy()   # make a copy of the table

# tidy_happiness_table.loc[:, 'Score'] = pd.to_numeric(tidy_happiness_table['Score'], errors='coerce')  # convert the Score column to numeric

# print(tidy_happiness_table)  # print the table

df = pd.DataFrame(happiness_table)
df.to_excel('happiness_report.xlsx', index=False)