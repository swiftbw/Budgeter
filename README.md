# Budgeter

Run Command:
From the ~/dev/Budgeter directory run:
python3 BActivity.py

Configuration:
The program takes B of A "My Financial Picture" download files and
Chase Activity Download files as input.

The main section of BActivity.py sets file locations for the
following:

Config Info:
      rootdir = os.environ['HOME'] # root directory for all input,
      output, and config files.
      budgetdir = rootdir + '/Library/Mobile Documents/com~apple~cloudDocs/Documents/Finances/BudgetTracking/'
      configdir = budgetdir + 'BudgeterConfig/'
      categfilename = configdir + 'CategoryMaps.csv'
      counterfilename = configdir + 'CounterpartyMaps.csv'
      vcfilename = configdir + 'BudgetCategories.csv'
      overridefilename = configdir + 'OverrideMaps.csv'
	  
Input and Output Data Files:
      datadir = 'BudgetData2023/'
      bofafilenames = ['ExportData-20230101-20230930_BofA.csv', 'ExportData-39.csv']
      chasefilenames = ['Chase1964_Activity20230101_20230630_20231008.CSV',
                        'Chase1964_Activity20230701_20230930_20231008.CSV',
                        'Chase1964_Activity20231001_20231008_20231008.CSV',
                        'Chase7536_Activity20230101_20230930_20231008.CSV',
                        'Chase7536_Activity20230101_20230930_20231008.CSV',
                        ]
                        
      budgetdatadir = budgetdir + datadir
      mbdfilename = budgetdatadir + 'MergedBudgetData.csv'

To prepare to run:
Download My Financial Picture Activity Data from B of A account.  Save
to appropriate directly.
Download Incremental activity data for credit cards from chase.  Note
the need to do incrementally -- they have a limit on the number of
records that can be downloaded.  Basically just download activity from
most recent quarter.

Once all downloads are complete and have been copied to the
appropriate directory, update the configuration variables listed above
in BActivity.py file.

Run script.
Check the following files to identify new counterparties that need to
be added.

Add new counterparties
Map new counterparties to categories 
	  
Logic is:

Load raw file.

Filter by Account
Credit Card
Checking Account

Create Category Element based on Transaction Filtering and append to
record.

Write out simplified file for each account including 

DateInstructions
Amount
Category
Counterparty

testing 123
testing 456

