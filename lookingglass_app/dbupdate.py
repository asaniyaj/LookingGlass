import sqlite3


def addImages(urlList, query_text):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()   
    print query_text
    tags= ""
    for t in query_text:
        print t, type(t), 
        t2 = str(t)
        print t2, type(t2), "random"
        t1 = t2.replace("'", "")
        tags = tags + " " + str(t1)
    print "tags", tags
    for url in urlList:
        print url, tags
        try:
            insertstat = "INSERT INTO lookingglass_app_image (url, tag,source) VALUES ('"+str(url)+"', '"+str(tags)+"', 'Google');";
            print insertstat
            c.execute(insertstat)
        except sqlite3.ProgrammingError as e:
            print e             
    conn.commit()
    conn.close()
    
