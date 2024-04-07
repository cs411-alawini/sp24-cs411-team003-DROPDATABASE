from utils import LocalSQL

sql_cur = LocalSQL()

# create table sample
insert_query = '''
CREATE TABLE sample (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);
'''
insert_params = {'name': "John Doe", 'email': "johndoe@example.com"}
rows_affected = sql_cur.execute(insert_query, insert_params)
print(f"Rows inserted: {rows_affected}")

# Insert a new record into the 'users' table
insert_query = "INSERT INTO sample (name, email) VALUES (:name, :email)"
insert_params = {'name': "John Doe", 'email': "johndoe@example.com"}
rows_affected = sql_cur.execute(insert_query, insert_params)
print(f"Rows inserted: {rows_affected}")

# Close the database connection
sql_cur.close()