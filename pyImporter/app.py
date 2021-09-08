import pymonetdb

qtdPerPage = 10

# import the SQL module
# set up a connection. arguments below are the defaults
monetdbConn = pymonetdb.connect(
    username="monetdb", password="monetdb", hostname="localhost", database="sciphy_dados")

# create a cursor
cursor = monetdbConn.cursor()

# increase the rows fetched to increase performance (optional)
cursor.arraysize = 100

limitString = ' LIMIT ' + str(qtdPerPage) + ' '

dataflowConsulta = 'SELECT id,tag,user_id FROM dataflow'
dataflowPage = 1

cursor.execute(
    'SELECT ceil(count(*)/' + str(qtdPerPage) + ') FROM (' + dataflowConsulta + ') x')
dataflowUltimaPagina = int(cursor.fetchone()[0])

while(dataflowPage <= dataflowUltimaPagina):
    dataflowOffset = ''

    if(dataflowPage > 1):
        dataflowOffset = ' OFFSET ' + str((dataflowPage-1) * qtdPerPage) + ' '
    else:
        # Show the table meta data
        dataflowMetadata = cursor.description

    cursor.execute(dataflowConsulta+limitString+dataflowOffset)
    dataflow = cursor.fetchall()

    dataflowPage += 1
