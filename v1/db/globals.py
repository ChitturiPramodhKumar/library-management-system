MYSQL_DB = 'library'
INVENTORY_TABLE = 'books_inventory_table'
BORROW_TABLE = 'borrowed_books'
#queries
SELECT_ALL_BOOKS = f'SELECT id as ID, book_name as `Book name`, author as Author, edition as Edition, description as Description, category as Category, created_at as `Created at`, count as Count, book_available as `No.of books available`, availability as Availability FROM {INVENTORY_TABLE}'

SELECT_BORROWED_BOOKS = f'SELECT borrow_id as `Borrow ID`,person_name as Person, contact_number as `Contact number`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE}'

def borrow_book_by_person(person, contact):
    SELECT_BORROWED_BOOKS_BY_PERSON = f'SELECT borrow_id as `Borrow ID`,person_name as Person, contact_number as `Contact number`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE person_name = "{person}" and contact_number = "{contact}"'
    return SELECT_BORROWED_BOOKS_BY_PERSON

REPORT_FROM_INVENTORY = f'SELECT id, book_name, author, edition, category, count, book_available, availability FROM {INVENTORY_TABLE}'

def borrow_report(book_id):
    REPORT_FROM_BORROWS = f"SELECT COUNT(book_id) as borrows FROM {BORROW_TABLE} WHERE book_id = '{book_id}' "
    return REPORT_FROM_BORROWS
def return_report(book_id):
    REPORT_FROM_BORROWS = f"SELECT COUNT(returned_at) as returns FROM {BORROW_TABLE} WHERE book_id = '{book_id}' and returned_at != '-'"
    return REPORT_FROM_BORROWS
# SELECT_ALL_BOOKS = f'select Id as ID, `Book name` as Title, Author as Author from {INVENTORY_TABLE}'

ADD_BOOK_TO_INVENTORY = f'INSERT INTO {INVENTORY_TABLE} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

ADD_BOOK_TO_BORROW = f'INSERT INTO {BORROW_TABLE} VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)'

def update(table_name, changes, condition):
    # UPDATE_BOOK_DATA = f'UPDATE {INVENTORY_TABLE} SET %s WHERE %s'
    query = f'UPDATE {table_name} SET {changes} WHERE {condition}'
    return query

def getstr(num):
    str = ''
    for i in range(num):
        str += '%s'
        if i < num-1:
            str += ', '
    return str

def delete_record(table_name, condition):
    query = f"DELETE FROM {table_name} WHERE {condition}"
    return query

def search_by_book_name(book_name, table_name, person, contact):
    if table_name == INVENTORY_TABLE:
        SEARCH = f"SELECT id as ID, book_name as `Book name`, author as Author, edition as Edition, description as Description, category as Category, created_at as `Created at`, count as Count, book_available as `No.of books available`, availability as Availability FROM {INVENTORY_TABLE} WHERE book_name = '{book_name}'"
    elif table_name == BORROW_TABLE:
        SEARCH = f"SELECT borrow_id as `Borrow ID`,person_name as Person, contact_number as `Contact number`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE book_name = '{book_name}' and person_name = '{person}' and contact_number = '{contact}'"   
    return SEARCH

def search_by_book_id(book_id, table_name, person, contact):
    if table_name == INVENTORY_TABLE:
        SEARCH = f"SELECT id as ID, book_name as `Book name`, author as Author, edition as Edition, description as Description, category as Category, created_at as `Created at`, count as Count, book_available as `No.of books available`, availability as Availability FROM {INVENTORY_TABLE} WHERE id = '{book_id}'"
    elif table_name == BORROW_TABLE:
        SEARCH = f"SELECT borrow_id as `Borrow ID`,person_name as Person, contact_number as `Contact number`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE book_id = '{book_id}'  and person_name = '{person}' and contact_number = '{contact}'"
    return SEARCH

def search_by_borrow_id(borrow_id, person, contact):
    SEARCH = f"SELECT borrow_id as `Borrow ID`,person_name as Person, contact_number as `Contact number`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE borrow_id = '{borrow_id}'  and person_name = '{person}' and contact_number = '{contact}'"
    return SEARCH
    
    
# INSERT_BOOK = 'INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'