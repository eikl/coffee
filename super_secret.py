#here we store secret stuff
DATABASE_URL = 'mysql+pymysql://admin:salasana@coffee-data.c1uqaxg5dghw.eu-north-1.rds.amazonaws.com:3306/srf05_data'
db = pymysql.connect(host='coffee-data.c1uqaxg5dghw.eu-north-1.rds.amazonaws.com', user='admin', password='salasana')