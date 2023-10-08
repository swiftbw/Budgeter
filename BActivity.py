'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os, datetime

class BActivity:
      def __init__(self, filestr = "", ftype = "None"):
            self._filename = filestr
            self._ftype = ftype
            self._headers = ['Date', 'Month', 'Counterparty', 'Category', 'Amount', 'Source', 'Orig_Cparty']
            self._max_header = 0
            self._indexes = []
            self._records = []
            self._inSources = ['Bank of America - Bank - Adv Tiered Interest Chkg', 'Bank of America - Credit Card - Premium Rewards Visa Signature', 'Chase']
            self._crecords = []
            self._current_header = []
            self._validCategories = ['Category', 'ATM', 'Auto', 'Charity', 'Deposits', 'Dining', 'Education', 'Entertainment', 'Fees', 'Fitness', 'Gas', 'Groceries', 'Health', 'Home', 'Insurance', 'Interest', 'Misc', 'Mortgage', 'Music Lessons', 'Paycheck', 'Payments', 'Pets', 'Shopping', 'Subscriptions', 'Taxes', 'Transfers', 'Travel', 'Unassigned', 'Utilities', 'GrandTotal' ]
            self._headerMap = {'CHASE' : {'Date' : 'Transaction Date', 'Counterparty' : 'Description', 'Category' : 'Category', 'Amount' : 'Amount', 'Source' : 'None', 'Orig_Cparty' : 'Description' }, 'BOFA' : {'Date' : 'Date', 'Counterparty' : 'Original Description', 'Category' : 'Category', 'Amount' : 'Amount', 'Source' : 'Account Name', 'Orig_Cparty' : 'Original Description' }}
            self._counterpartyMaps = { '*AMZN' : 'Amazon',
                                             '*MARSHALLS' : 'Marshalls',
                                             '*VALLI' : 'Valli',
                                             '*Amazon.com' : 'Amazon',
                                             '*STARBUCKS' : 'Starbucks',
                                             '*BMOH' : 'ATM',
                                             '*MIOMA' : 'Personal Trainer',
                                             '*PHLVARIABLE' : 'Phoenix Life Insurance',
                                             '*CUBESMART' : 'Cube Smart Storage',
                                             '*WHOLEFDS' : 'Whole Foods',
                                             '*TJMAXX' : 'TJ Maxx',
                                             '*EXXON' : 'Exxon',
                                             '*DES:MORTGAGE' : 'Mortgage',
                                             '*ATM Oper Rebate' : 'ATM Refund',
                                             '*College Savings' : 'Noah 529',
                                             '*CHASE CREDIT CRD' : 'Chase Card Payment',
                                             '*WALGREENS' : 'Walgreens',
                                             '*TRADER JOE' : 'Trader Joes',
                                             '*ALDI' : 'Aldi',
                                             '*DES:BANK OF AM ID:xxxxxxxxxx0495' : 'Paycheck',
                                             '*ATM Wthdrwl Fee Waiver' : 'ATM Fee Waiver',
                                             '*COMED            DES' : 'ComEd',
                                             '*365 Market' : '365 Market',
                                             '*MCDONALD' : 'McDonalds',
                                             '*FRESH MARKET' : 'Tonys Fresh Market',
                                             '*SHELL OIL' : 'Shell Oil',
                                             '*BRK 2717' : 'Merrill LOC',
                                             '*GOODWILL' : 'Good Will',
                                             '*JEWEL' : 'Jewel Osco'
                                             }
            self._categoryMaps = { 'Amazon':'Shopping',
                                             'Marshalls':'Shopping',
                                             'Valli':'Groceries',
                                             'Amazon':'Shopping',
                                             'Starbucks':'Dining',
                                             'ATM':'Cash Withdrawals',
                                             'Personal Trainer':'Fitness',
                                             'Phoenix Life Insurance':'Insurance',
                                             'Cube Smart Storage':'Utilities',
                                             'Whole Foods':'Groceries',
                                             'TJ Maxx':'Shopping',
                                             'Exxon':'Gas',
                                             'Mortgage':'Mortgage',
                                             'ATM Refund':'Cash Withdrawals',
                                             'Noah 529':'Education',
                                             'Chase Card Payment':'Transfers',
                                             'Walgreens':'Health',
                                             'Trader Joes':'Groceries',
                                             'Aldi':'Groceries',
                                             'Paycheck':'Income',
                                             'ATM Fee Waiver':'Cash Withdrawals',
                                             'ComEd':'Utilities',
                                             '365 Market':'Groceries',
                                             'McDonalds':'Dining',
                                             'Tonys Fresh Market':'Groceries',
                                             'Shell Oil':'Gas',
                                             'Good Will':'Shopping',
                                             'Jewel Osco':'Groceries'
                                             }
            self._overrideMaps = {}

            if (self._filename != ""):
                  with open(self._filename, mode='r', encoding = 'utf-8-sig') as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        line_count = 0
                        for row in csv_reader:
                              cdentry = {}
                              for key in self._headers:
                                    if key == 'Month':
                                          dt = row[self._headerMap[self._ftype]['Date']]
                                          dto = datetime.datetime.strptime(dt, '%m/%d/%Y')
                                          month = dto.strftime('%b')
                                          cdentry[key] = month
                                    else:
                                          if key != 'Source':
                                                cdentry[key] = row[self._headerMap[self._ftype][key]]
                                          else:
                                                if self._ftype == 'CHASE':
                                                      cdentry[key] = "Chase"
                                                else:
                                                      cdentry[key] = row[self._headerMap[self._ftype][key]]
                              self._crecords.append(cdentry)
                              self._records.append(row)
                              if line_count == 0:
                                    line_count += 1
                              else:
                                    line_count += 1
                  print(f'Processed {line_count} lines.')
            else:
                  print('BActivity object created with no filename.')
      def getRecords(self):
            return self._crecords
      def load(self, crecords):
            for record in crecords:
                  self._crecords.append(record)
      def pruneSources(self):
            nrecords = []
            
            for record in self._crecords:
                  if record['Source'] in self._inSources:
                        nrecords.append(record)
            self._crecords = nrecords
      def write ( self, filename ):
            try:
                  filehandle = open(filename, "w")

                  filehandle.write ('"' + '","'.join(self._headers) + '"\n')

                  for i in self._crecords:
                        filehandle.write ('"' + '","'.join(i.values()) + '"\n')
                        
                  filehandle.close()
            except:
                  print ( "ERROR in write except\n" )
      def updateCounterparties ( self ):
            for row in self._crecords:
                  for pattern in self._counterpartyMaps:
                        if WCMatch ( row [ 'Counterparty' ], pattern ):
                              row [ 'Counterparty' ] = self._counterpartyMaps [ pattern ]
            return
      def uploadCounterpartyMaps ( self, filename ):
            map = self.uploadMaps ( filename )
            self._counterpartyMaps = {}
            for i in map:
                  self._counterpartyMaps[i['Counterparty']] = i['Map']
            return

      def updateCategories ( self ):
            for row in self._crecords:
                  row [ 'Category' ] = 'Unassigned'
                  for pattern in self._categoryMaps:
                        if WCMatch ( row [ 'Counterparty' ], pattern ):
                              row [ 'Category' ] = self._categoryMaps [ pattern ]
            return
      def uploadCategoryMaps ( self, filename ):
            map = self.uploadMaps ( filename )
            self._categoryMaps = {}

            for i in map:
                  ky = i['Counterparty']
                  vl = i['Category']

                  if ( self._validCategories.count ( vl ) != 0 ):
                        self._categoryMaps[i['Counterparty']] = i['Category']
                  else:
                        print ( 'Unable to find Category ' + vl + ' in valid Categories in Category Map entry:  ' + ky + ', ' + vl + '.  Excluding.' )
            return
      
      def getValidCategories ( self, filename ):
            map = self.uploadMaps ( filename )
            self._validCategories = []

            print ("Uploading Categories from; "+filename)

            for i in map:
                  vl = i['Category']
                  print ('DEBUG: ' + 'Valid Category uploaded:  ' + vl )
                  self._validCategories.append ( i['Category'] )
            return

      def applyOverrides ( self ):
            return
      
      def uploadOverrides ( self, filename ):
            map = self.uploadMaps ( filename )
            self._overrideMaps = {}
            
      def uploadMaps ( self, filename ):
            map = []
            with open(filename, mode='r', encoding='utf-8-sig') as csv_file:
                  csv_reader = csv.DictReader(csv_file)
                  line_count = 0
                  for row in csv_reader:
                        map.append(row)
            csv_file.close
            return map

def WCMatch ( instr = "", pattern = "" ):
      response = True
      if pattern[0] == '*':
            wildcard = True
            pattern = pattern[1:]

      if instr.find(pattern) == -1:
            return False
      else:
            return True

def main():
      filename = os.environ['HOME']
      filename += '/Library/Mobile Documents/com~apple~cloudDocs/Documents/Finances/BudgetTracking/'
      cfilename = filename + 'BudgeterConfig/'
      catfilename = cfilename + 'CategoryMaps.csv'
      countfilename = cfilename + 'CounterpartyMaps.csv'
      vcfilename = cfilename + 'BudgetCategories.csv'
      overfilename = cfilename + 'OverrideMaps.csv'
      #dirname = 'BudgetData2022/'
      #bofafilename = 'ExportData-36.csv'
      #chasefilename = 'Chase9789_Activity2022.CSV'
      dirname = 'BudgetData2023/'
      bofafilenames = ['ExportData-20230101-20230930_BofA.csv', 'ExportData-39.csv']
      chasefilenames = ['Chase1964_Activity20230101_20230630_20231008.CSV',
                        'Chase1964_Activity20230701_20230930_20231008.CSV',
                        'Chase1964_Activity20231001_20231008_20231008.CSV',
                        'Chase7536_Activity20230101_20230930_20231008.CSV',
                        'Chase7536_Activity20230101_20230930_20231008.CSV',
                        
      iofilename = filename + dirname
      ofilename = iofilename + 'MergedBudgetData.csv'
      print (catfilename + '\n' + countfilename + '\n' + overfilename + '\n' )
      a = BActivity()
      for fn in bofafilenames:
            b = BActivity(iofilename+fn, 'BOFA')
            a.load(b.getRecords())
      for fn in chasefilenames:
            c = BActivity(iofilename+fn, 'CHASE')
            a.load(c.getRecords())
      
      a.pruneSources()
      a.uploadCounterpartyMaps ( countfilename )
      a.getValidCategories ( vcfilename )
      a.uploadCategoryMaps ( catfilename )
      a.uploadOverrides ( overfilename )
      a.updateCounterparties ( )
      a.updateCategories ( )
      a.applyOverrides ( )
      a.write ( ofilename )

if __name__ == "__main__":
      main()
