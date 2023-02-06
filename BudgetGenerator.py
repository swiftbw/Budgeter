'''
Flow of the program should be as follows:
1.  Load B of A and Chase Spreadsheets
2.  Filter out info from unwanted accounts (Merrill stuff, for example)
3.  Merge B of A and Chase spreadsheets into common format
4.  Load Counterparty Conversion file
5.  Convert Counterparties to desired Counterparty representation
6.  Compute Category for each row.
7.  Write merged, converted output file.
'''

 def main():
      filename = os.environ['HOME']
      filename += '/dev/BudgeterData/'
      chaseInputFilename = filename + 'ExportData-35.csv'
      bofaInputFilename = filename + 'Chase9789_Activity20230204.CSV'
      BudgetOutputFilename = filename + 'BudgetFile.csv'
      chaseExtract = BActivity(chaseInputFilename, 'CHASE')
      bofaExtract = BActivity(bofaInputFilename, 'BOFA')

      clist = chaseExtract.chaseConvert()
      blist = bofaExtract.bofaConvert()
      
      
if __name__ == '__main__':
      main()
