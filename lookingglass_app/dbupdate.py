import sqlite3


def addImages(urlList, tags):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()   
    for url in urlList:
        print url, tags
        try:
            #insert if not exists
            #insertstat = "INSERT INTO lookingglass_app_image (url, tag,source) VALUES ('"+str(url)+"', '"+str(tags)+"', 'Google');";
            
            insertstat = "INSERT INTO lookingglass_app_image (url, tag,source) SELECT '" + str(url) + "', '" + str(tags) + "', 'Google' WHERE NOT EXISTS(SELECT 1 FROM lookingglass_app_image WHERE url = '" + str(url) + "');"            
            print insertstat
            c.execute(insertstat)
        except sqlite3.ProgrammingError as e:
            print e             
    conn.commit()
    conn.close()
    
