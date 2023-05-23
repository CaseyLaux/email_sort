import pandas as pd
results = pd.read_csv('./results.csv', encoding='latin-1')
results[results['classification/accuracy'].notnull()].tail(1)

results[results['classification/accuracy'].notnull()]['classification/accuracy'].plot()
