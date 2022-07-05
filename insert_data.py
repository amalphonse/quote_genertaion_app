from sqlalchemy import create_engine
my_conn = create_engine("postgresql://localhost:5432/quotes_api")


query="INSERT INTO quotes (quote, author, author_details_id) \
VALUES(%s,%s,%s)"

my_data=[('A mistake repeated more than once is a decision', 'Paulo Coelho',1),
        ('Don’t waste your time with explanations: people only hear what they want to hear', 'Paulo Coelho',1),
        ( 'To heal a wound you must stop scratching it', 'Paulo Coelho', 1)]
    
id=my_conn.execute(query,my_data)

#id=my_conn.execute("INSERT INTO quotes (id, quote, author) \
#VALUES (1,'A mistake repeated more than once is a decision', 'Paulo Coelho');")
#id=my_conn.execute("INSERT INTO authorDetails (name, birth_year, career, about) \
#VALUES ('Paulo Coelho',1947,'writer','The Alchemist');")

#id=my_conn.execute("INSERT INTO quotes (id, quote, author) \
##VALUES (2, 'Don’t waste your time with explanations: people only hear what they want to hear', 'Paulo Coelho');\
#")

#id=my_conn.execute("INSERT INTO quotes (id, quote, author, author_details_id) \
#VALUES (3, 'To heal a wound you must stop scratching it', 'Paulo Coelho', 1);\
#")

print("Row Added  = ",id.rowcount)