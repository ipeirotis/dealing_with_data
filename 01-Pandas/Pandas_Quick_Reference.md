# Pandas Quick Reference Guide
## For Business Students with SQL Background

---

## Core Data Structures

| Structure | Description | SQL Equivalent |
|-----------|-------------|----------------|
| **DataFrame** | 2D table with rows and columns | Table or query result |
| **Series** | Single column of data | One column |
| **Index** | Row labels (usually 0, 1, 2...) | Row IDs |

---

## Loading Data

```python
# From SQL database (BigQuery)
df = client.query("SELECT * FROM table").to_dataframe()

# From CSV file
df = pd.read_csv("file.csv")

# From Excel file
df = pd.read_excel("file.xlsx", sheet_name="Sheet1")

# From URL
df = pd.read_csv("https://example.com/data.csv")
```

---

## Exploring Data

| Method | Purpose | Example |
|--------|---------|---------|
| `df.head(n)` | First n rows | `df.head(10)` |
| `df.tail(n)` | Last n rows | `df.tail(5)` |
| `df.sample(n)` | Random n rows | `df.sample(10)` |
| `df.shape` | (rows, columns) | `df.shape` → (1000, 8) |
| `len(df)` | Number of rows | `len(df)` → 1000 |
| `df.columns` | Column names | `list(df.columns)` |
| `df.dtypes` | Data types | `df.dtypes` |
| `df.info()` | Overview | `df.info()` |

---

## SQL to Pandas Translation

### SELECT columns
```sql
-- SQL
SELECT col1, col2 FROM table
```
```python
# Pandas
df.filter(items=['col1', 'col2'])
# or
df[['col1', 'col2']]
```

### SELECT with alias (AS)
```sql
-- SQL
SELECT col1 AS new_name FROM table
```
```python
# Pandas
df.rename(columns={'col1': 'new_name'})
```

### WHERE (filter rows)
```sql
-- SQL
SELECT * FROM table WHERE col > 10
SELECT * FROM table WHERE col = 'value'
SELECT * FROM table WHERE col IN ('a', 'b', 'c')
```
```python
# Pandas
df.query('col > 10')
df.query('col == "value"')
df.query('col in ["a", "b", "c"]')
```

### ORDER BY
```sql
-- SQL
SELECT * FROM table ORDER BY col DESC
```
```python
# Pandas
df.sort_values('col', ascending=False)
```

### DISTINCT
```sql
-- SQL
SELECT DISTINCT col FROM table
```
```python
# Pandas
df['col'].drop_duplicates()
# or for multiple columns
df.filter(items=['col1', 'col2']).drop_duplicates()
```

### LIMIT
```sql
-- SQL
SELECT * FROM table LIMIT 10
```
```python
# Pandas
df.head(10)
```

### JOIN
```sql
-- SQL
SELECT * FROM t1 JOIN t2 ON t1.key = t2.key
```
```python
# Pandas
pd.merge(t1, t2, on='key', how='inner')
# For different column names:
pd.merge(t1, t2, left_on='key1', right_on='key2', how='inner')
```

### GROUP BY with aggregation
```sql
-- SQL
SELECT col, AVG(val), COUNT(*) 
FROM table 
GROUP BY col
```
```python
# Pandas
df.groupby('col').agg(
    avg_val=('val', 'mean'),
    count=('val', 'count')
)
```

---

## Descriptive Statistics

### For Numeric Columns

| Method | Returns |
|--------|---------|
| `df['col'].describe()` | count, mean, std, min, 25%, 50%, 75%, max |
| `df['col'].mean()` | Average |
| `df['col'].median()` | Median (50th percentile) |
| `df['col'].std()` | Standard deviation |
| `df['col'].min()` | Minimum |
| `df['col'].max()` | Maximum |
| `df['col'].sum()` | Total |

### For Categorical Columns

| Method | Returns |
|--------|---------|
| `df['col'].value_counts()` | Count of each unique value |
| `df['col'].nunique()` | Number of unique values |
| `df['col'].unique()` | Array of unique values |

---

## Visualization Quick Reference

```python
# Histogram (numeric data)
df['col'].hist(bins=30)

# Bar chart (categorical data)
df['col'].value_counts().plot(kind='bar')

# Horizontal bar (easier to read labels)
df['col'].value_counts().head(10).plot(kind='barh')

# Line plot
df.plot(kind='line', x='date', y='value')

# Scatter plot
df.plot(kind='scatter', x='col1', y='col2')

# KDE (smoothed histogram)
df['col'].plot(kind='kde')
```

---

## Method Chaining Pattern

Combine multiple operations in one readable statement:

```python
(
    df
    .query('condition')           # Filter rows
    .filter(items=['col1','col2']) # Select columns
    .drop_duplicates()            # Remove duplicates
    .sort_values('col1')          # Sort
    .head(10)                     # Limit rows
)
```

---

## Pivot Tables

Create multi-dimensional summaries:

```python
pd.pivot_table(
    data=df,
    index='row_var',        # What goes in rows
    columns='col_var',      # What goes in columns (optional)
    values='value_var',     # What to aggregate
    aggfunc='mean'          # How to aggregate
)
```

**Common aggfunc values:** `'mean'`, `'sum'`, `'count'`, `'min'`, `'max'`, `'std'`

---

## Time Series Operations

### Resampling (change time granularity)

```python
# Assumes index is datetime
df.resample('D').mean()   # Daily
df.resample('W').sum()    # Weekly
df.resample('M').mean()   # Monthly
df.resample('Q').sum()    # Quarterly
df.resample('Y').mean()   # Yearly
```

---

## Creating New Columns

### Simple expressions
```python
df.assign(new_col = df['col1'] + df['col2'])
```

### Using functions
```python
def my_function(df):
    return df['col1'] * 2

df.assign(new_col = my_function)
```

### Applying to each row
```python
def process_row(row):
    return row['col1'] + row['col2']

df['new_col'] = df.apply(process_row, axis='columns')
```

---

## Common Patterns

### Filter, then analyze
```python
(
    df
    .query('BORO == "Manhattan"')
    ['SCORE']
    .describe()
)
```

### Group, aggregate, then sort
```python
(
    df
    .groupby('category')
    .agg(avg=('value', 'mean'), count=('value', 'count'))
    .sort_values('avg', ascending=False)
)
```

### Normalize to percentages
```python
# Column totals sum to 1
normalized = df / df.sum()

# Row totals sum to 1
normalized = df.div(df.sum(axis=1), axis=0)
```

---

## Data Types

| Pandas dtype | Description | Example |
|--------------|-------------|---------|
| `int64` | Integer | 1, 42, -7 |
| `float64` | Decimal | 3.14, -2.5 |
| `object` | Text/string | "Hello" |
| `datetime64` | Date/time | 2024-01-15 |
| `bool` | True/False | True |

### Check types
```python
df.dtypes
```

### Convert types
```python
df['col'] = df['col'].astype(int)
df['col'] = pd.to_datetime(df['col'])
```

---

## Handling Missing Data

```python
# Check for missing values
df.isna().sum()

# Drop rows with any missing values
df.dropna()

# Drop rows where specific column is missing
df.dropna(subset=['col'])

# Fill missing values
df.fillna(0)
df.fillna(df['col'].mean())
```

---

## Quick Tips

1. **Always explore first:** `df.head()`, `df.info()`, `df.describe()`

2. **Use chain notation** for readable multi-step operations

3. **Most operations return new DataFrames** — assign to save:
   ```python
   df_filtered = df.query('condition')
   ```

4. **Use `.copy()` to avoid warnings** when modifying subsets:
   ```python
   subset = df.query('condition').copy()
   ```

5. **For string matching:** Use `.str` accessor:
   ```python
   df.query('col.str.contains("pattern")')
   ```

---

## Resources

- **Official Documentation:** [pandas.pydata.org](https://pandas.pydata.org/docs/)
- **Cheat Sheet:** [Pandas Cheat Sheet PDF](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- **10 Minutes to Pandas:** [Quick Tutorial](https://pandas.pydata.org/docs/user_guide/10min.html)
