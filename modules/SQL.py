import os, sys
import sqlite3

SQL = None
sqlCursor = None

#return dictionary from sqlite3 query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#return list of dictionaries for all entries in database
def getPackages():
    global SQL, sqlCursor
    return sqlCursor.execute( 'SELECT * FROM packages' ).fetchall()

#return all packages of a certain type
def getPackageByType( packageType, args ):
    global SQL, sqlCursor
    d = sqlCursor.execute( 'SELECT * FROM packages WHERE type LIKE (?)', (packageType,) ).fetchall()
    return d

#entryDict = {'date':date, 'time':time, 'size':size, 'type':type, 'image':image, 'weight':weight, 'other':other}
def registerPackage( entryDict ):
    global SQL, sqlCursor
    query = ('INSERT or REPLACE INTO packages '
             '(date, time, size, type, image, weight, other) '
             'VALUES (:date, :time, :size, :type, :image, :weight, :other)')
    sqlCursor.execute( query, entryDict )
    SQL.commit()

#clear database
def clearDatabase():
    global SQL, sqlCursor
    sqlCursor.execute( 'DELETE FROM packages' )
    SQL.commit()

#delete entry from database
def deleteEntry( entryID ):
    global SQL, sqlCursor
    query = ('DELETE FROM packages '
                    'where id=:id')
    sqlCursor.execute( query, entryID )
    SQL.commit()

#package = (date, time, size, type, image, other),(...)
def registerPackage( package ):
    global SQL, sqlCursor
    query = ('INSERT INTO packages '
                    '(date, time, size, type, image, weight, other) '
                    'VALUES (:date, :time, :size, :type, :image, :weight, :other)')
    sqlCursor.execute( query, package )
    SQL.commit()

#convert image to blob
def getImageBlob( imagePath ):
    try:
        with open( imagePath, 'rb' ) as file:
            return file.read()
    except:
        return None
    
def getDatabasePath ( defaultPath = './config/' ):
    if __name__ == "__main__":
        defaultPath = '../'
    global SQL, sqlCursor
    path = os.path.realpath( defaultPath )
    if not os.path.isdir( path ):
        defaultPath = os.path.realpath( os.path.dirname(sys.argv[0]) )
        path = os.path.join( defaultPath,'config' )
    return os.path.join( path, 'config.db3' )

#load credentials database and return credentials as dictionary
def loadCredentials():
    sqlCredentials = sqlite3.connect( "./credentials.db3", check_same_thread=False )
    sqlCredentials.row_factory = dict_factory
    credentialsCursor = sqlCredentials.cursor()
    credentials = credentialsCursor.execute( 'SELECT * FROM credentials' ).fetchall()
    return credentials


def init():
    global SQL, sqlCursor
    DATABASE_PATH = getDatabasePath()
    SQL = sqlite3.connect( DATABASE_PATH, check_same_thread=False )
    SQL.row_factory = dict_factory
    sqlCursor = SQL.cursor()

    #Create database table
    sqlCursor.execute( 'CREATE TABLE IF NOT EXISTS packages ' 
                        '(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,'
                        'date TEXT, time TEXT, size TEXT, type TEXT,' 
                        'image BLOB, weight NUMERIC,other INTEGER)' )
    SQL.commit()

if __name__ == "__main__":
    #test the module
    init()
    print("Registering packages...")
    registerPackage( {'date':'2021-01-01', 'time':'12:00', 'size':'small', 'type':'letter', 'image':None, 'weight':0.5, 'other':0})
    
    print("Package registered: ")
    packages = getPackages()
    print(f"Number of packages: {len(packages)}")
    print( packages )

    #clearDatabase()
    print("cleaning database...")
    #get last package and delete it by id
    deleteEntry( packages[-1] )
    packages = getPackages()
    print(f"Number of packages: {len(packages)}")
    print( packages )
    SQL.close()
