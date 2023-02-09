'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os

class BActivity:
      def __init__(self, filestr = "", ftype = "None"):
            self._filename = filestr
            self._ftype = ftype
            self._headers = ['Date', 'Counterparty', 'Category', 'Amount', 'Source', 'Orig_Cparty']
            self._max_header = 0
            self._indexes = []
            self._records = []
            self._inSources = ['Bank of America - Bank - Adv Tiered Interest Chkg', 'Bank of America - Credit Card - Premium Rewards Visa Signature', 'Chase']
            self._crecords = []
            self._current_header = []
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
            self._counterpartyOverrides = {}
            
            with open(self._filename, mode='r') as csv_file:
                  csv_reader = csv.DictReader(csv_file)
                  line_count = 0
                  for row in csv_reader:
                        cdentry = {}
                        for key in self._headers:
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
                  print(len(self._records))
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
                  self._categoryMaps[i['Counterparty']] = i['Category']
                                              
            return
      def updateOverrides ( self ):
            return
      def uploadOverrideMaps ( self, filename ):
            return
      def uploadMaps ( self, filename ):
            map = []
            with open(filename, mode='r') as csv_file:
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
      filename += '/dev/BudgeterData/'
      bfilename = filename + 'ExportData-35.csv'
      cfilename = filename + 'Chase9789_Activity20230204.CSV'
      ofilename = filename + 'MergedBudgetData.csv'
      catfilename = filename + 'CategoryMaps.csv'
      countfilename = filename + 'CounterpartyMaps.csv'
      overfilename = filename + 'OverrideMaps.csv'
      a = BActivity(bfilename, 'BOFA')
      b = BActivity(cfilename, 'CHASE')
      a.load(b.getRecords())
      a.pruneSources()
      a.uploadCounterpartyMaps(countfilename)
      a.uploadCategoryMaps(catfilename)
      a.updateCounterparties()
      a.updateCategories()
      a.write(ofilename)

if __name__ == "__main__":
      main()
