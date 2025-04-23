'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os, datetime
import BudgetUtils

class BActivity:
      def __init__(self, filestr = "", ftype = "None"):
            '''
            BActivity class holds a list of expense records.
            If no filename is provided the object is initialized with no filename then no records are loaded.
            If a filename is provided then the corresponding file (in csv format) is attempted.
            '''
            self._filename = filestr
            self._ftype = ftype
            self._headers = ['Date', 'Month', 'Counterparty', 'Category', 'Amount', 'Source', 'Orig_Cparty']
            self._max_header = 0
            self._indexes = []
            self._records = []
            self._inSources = [      'Bank of America - Bank - Adv Tiered Interest Chkg',
                                     'Bank of America - Credit Card - Premium Rewards Visa Signature',
                                     'Chase']
            self._crecords = []
            self._current_header = []
            self._validCategories = ['Category',
                                           'ATM',
                                           'Auto',
                                           'Charity',
                                           'Deposits',
                                           'Dining',
                                           'Education',
                                           'Entertainment',
                                           'Fees',
                                           'Fitness',
                                           'Gas',
                                           'Groceries',
                                           'Health',
                                           'Home',
                                           'Insurance',
                                           'Interest',
                                           'Misc',
                                           'Mortgage',
                                           'Music Lessons',
                                           'Paycheck',
                                           'Pets',
                                           'Shopping',
                                           'Subscriptions',
                                           'Taxes',
                                           'Transfers',
                                           'Travel',
                                           'Unassigned',
                                           'Utilities',
                                           'GrandTotal' ]
            self._headerMap = {      'CHASE' :
                                     {
                                           'Date' : 'Transaction Date',
                                           'Counterparty' : 'Description',
                                           'Category' : 'Category',
                                           'Amount' : 'Amount',
                                           'Source' : 'None',
                                           'Orig_Cparty' : 'Description'
                                     },
                                     'BOFA' :
                                     {
                                           'Date' : 'Date',
                                           'Counterparty' : 'Original Description',
                                           'Category' : 'Category',
                                           'Amount' : 'Amount',
                                           'Source' : 'Account Name',
                                           'Orig_Cparty' : 'Original Description'
                                     }
                              }
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
            self._budgetMaps = {}
            self._overrideMaps = {}

            if (self._filename != ""):
                  line_count = 0
                  try:
                        with open(self._filename, mode='r', encoding = 'utf-8-sig') as csv_file:
                              csv_reader = csv.DictReader(csv_file)
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
                              csv_file.close()
                  except:
                        print (f'Unable to process {self._filename}.  Continuing')
                  print(f'Processed {line_count} lines.')
            else:
                  print('BActivity object created with no filename.')

      def getRecords(self, categ=None):
            ''' 
            getRecords returns the list of account entries that match the categ argument, or all records if categ is not provided.
            '''
            recs = []
            if categ == None:
                  return self._crecords
            else:
                  for i in self._crecords:
                        if categ == i['Category']:
                              recs.append(i)
                  return recs
      def load(self, crecords):
            dupecount = 0
            for record in crecords:
                  if self.contains(record):
                        dupecount += 1
                  self._crecords.append(record)
            print ( str(dupecount) + " records found and loaded.\n")
      def contains(self, newrecord):
            for record in self._crecords:
                  if record == newrecord:
                        return True
            return False
      def pruneSources(self):
            nrecords = []
            
            for record in self._crecords:
                  if record['Source'] in self._inSources:
                        nrecords.append(record)
            self._crecords = nrecords
      def write ( self, filename, cols=None ):
            if cols == None:
                  try:
                        filehandle = open(filename, 'w' )

                        filehandle.write ('"' + '","'.join(self._headers) + '"\n')

                        for i in self._crecords:
                              filehandle.write ('"' + '","'.join(i.values()) + '"\n')
                        
                        filehandle.close()
                  except:
                        print ( "ERROR in write except\n" )
            else:
                  try:
                        filehandle = open(filename, 'w')

                        filehandle.write ('"' + '","'.join(cols) + '"\n')

                        for i in self._crecords:
                              vals = []
                              for j in cols:
                                    vals.append(i[j])
                              filehandle.write ('"' + '","'.join(vals) + '"\n')
                        
                        filehandle.close()
                  except:
                        print ( "ERROR in write except\n" )
      def updateCounterparties ( self, bmap ):
            for row in self._crecords:
                  row [ 'Counterparty' ] = bmap.getMappedCounterparty ( row [ 'Counterparty' ] )
            return
      def writeRecordsForCat ( self, filename, cat = None, keys = [ 'Counterparty', 'Counterparty', 'Category'] ):
            ''' 
            writeRecordsForCat loops through all records and writes specified attributes for all records matching category. 
            '''
            print ( "In Write Budget Maps\n")

            try:
                  filehandle = open(filename, 'w')
                  
                  strn ='"' + '","'.join([str(ele) for ele in keys]) +'"\n'

                  filehandle.write ( strn )      

                  for i in self._crecords:
                        if cat != None and cat != i['Category']:
                              continue
                        strn ='"' + '","'.join([str(i[ele]) for ele in keys]) +'"\n'
                        filehandle.write ( strn )
                  filehandle.close()
            except Exception as e:
                  print ( e )
                  print ( "ERROR in writeBudgetMaps except\n" )
      def writeBudgetMaps ( self, filename, cat = None ):
            ''' 
            writeBudgetMaps loops through the counterpartyMaps dictionary, first extracting 
            '''
            print ( "In Write Budget Maps\n")

            for i in self._counterpartyMaps:
                  cpty = self._counterpartyMaps.get(i)
                  if cpty == None:
                        print ( 'Cannot find ' + i + ' in cptymap.  skipping\n')
                        continue
                  
                  ctgy = self._categoryMaps.get(cpty)
                  if ctgy == None:
                        print ( 'Cannot find ' + cpty + ' in ctgymap.  skipping\n')
                        continue
                  self._budgetMaps[i] = ( cpty, ctgy )
            try:
                  filehandle = open(filename, 'w')
                  
                  filehandle.write ('CPartyMatch,Counterparty,Category\n')

                  for i in self._budgetMaps:
                        bmval = self._budgetMaps.get(i)
                        if bmval == None:
                              print ( "bmval is None!\n" )
                              continue
                        strn = '"' + i + '","' + bmval[0] + '","' + bmval[1]+'"\n'
                        if strn == None:
                              print ( "None string!\n")
                        filehandle.write ( strn )
                  filehandle.close()
            except Exception as e:
                  print ( e )
                  print ( "ERROR in writeBudgetMaps except\n" )
      def updateCategories ( self, bmap ):
            for row in self._crecords:
                  row [ 'Category' ] = 'Unassigned'
                  row [ 'Category' ] = bmap.getMappedCategory ( row [ 'Counterparty' ] )
            return
      
      def getValidCategories ( self, filename ):
            map = self.uploadMaps ( filename )
            self._validCategories = []

            print ("Uploading Valid Categories from; "+filename)

            for i in map:
                  vl = i['Category']
                  self._validCategories.append ( i['Category'] )
            return

      def applyOverrides ( self ):
            return
      
      def uploadOverrides ( self, filename ):
            map = self.uploadMaps ( filename )
            self._overrideMaps = {}
            
      def uploadMaps ( self, filename ):
            map = []
            map = BudgetUtils.getCsvFileAsList ( filename )

            return map

def main():
      rootdir = os.environ['HOME'] # root directory for all input, output, and config files.
      budgetdir = rootdir + '/Library/Mobile Documents/com~apple~cloudDocs/Documents/Finances/BudgetTracking/'
      configdir = budgetdir + 'BudgeterConfig/'
      bmapfilename = configdir + 'BudgetMap.csv'
      categfilename = configdir + 'CategoryMaps.csv'
      counterfilename = configdir + 'CounterpartyMaps.csv'
      vcfilename = configdir + 'BudgetCategories.csv'
      overridefilename = configdir + 'OverrideMaps.csv'

if __name__ == "__main__":
      main()
