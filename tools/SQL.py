import sqlite3
from collections import defaultdict

class Database:
    def __init__(self, path):
        self.path = path
        self.cursor = sqlite3.connect(path)

    def execute(self, command, *args):
        '''Method for execute commands
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        with self.cursor:
            return self.cursor.execute(command, args)

    def create_table(self, table, *columns):
        if len(columns) == 0: raise ValueError('Insufficient data. At least one column must be specified.')
        if len(columns) == 1: columns = (str(columns)[:-2]+')')
        command = f'''
        CREATE TABLE IF NOT EXISTS "{table}" {columns};
        '''
        self.execute(command)

    def add_column(self, table, *columns_without_type, **columns_type):
        if len(columns_type) == 0 and len(columns_without_type) == 0: raise ValueError('Insufficient data. At least one column must be specified.')
        if len(columns_type) == 1: columns_type = (str(columns_type)[:-2]+')')
        columns_type = columns_type | {column: '' for column in columns_without_type}
        commands = [f'''ALTER TABLE {table} ADD COLUMN {column} {columns_type[column]};''' for column in columns_type]
        for command in commands:
            self.execute(command)

    def add_string(self, table, **string_of_column):
        if len(string_of_column) == 0: raise ValueError('Insufficient data. At least one column-line must be specified.')
        command = f'''
        INSERT OR IGNORE INTO {table} ({str([column for column in string_of_column])[1:-1].replace("'", '')})
        VALUES ({str([string_of_column[column] for column in string_of_column])[1:-1]})
        '''
        self.execute(command)

    def rename_table(self, table, new_name):
        command = f'''
        ALTER TABLE {table}
        RENAME TO {new_name};
        '''
        self.execute(command)

    def rename_column(self, table, old_name, new_name):
        command = f'''
        ALTER TABLE {table}
        RENAME COLUMN {old_name} TO {new_name};
        '''
        self.execute(command)

    def rename_cell(self, table, column='', value='', column_filter='', column_filter_value='', **kwargs):
        '''first the column with the new value, then the filter'''
        if not column and not value and not column_filter and not column_filter_value and len(kwargs)<2: raise ValueError('Not enough input. You need to specify the column name, new value, which column to filter on and the filter value.')
        if bool(column) != bool(value) or bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify two parameters at once, you can\'t just one.')
        if not column and len(kwargs)==0: raise ValueError('Not enough input.')
        if len(kwargs)>2: raise ValueError('Insufficient data. It is too many values.')
        if len(kwargs)==1 and column:
            column_filter = next(iter(kwargs))
            column_filter_value = kwargs[next(iter(kwargs))]
        elif len(kwargs)==1 and not column:
            column = next(iter(kwargs))
            value = kwargs[next(iter(kwargs))]
        elif len(kwargs)==2:
            kws = [(column, kwargs[column]) for column in kwargs]
            column=kws[0][0]
            value=kws[0][1]
            column_filter=kws[1][0]
            column_filter_value=kws[1][1]
        if column_filter[:5]=='__i__':
            column_filter = column_filter[5:]
        else:
            column_filter_value = f"'{column_filter_value}'"
        command = f'''
        UPDATE {table}
        SET {column} = "{value}"
        WHERE {column_filter} = {column_filter_value}
        '''
        self.execute(command)

    def delete_table(self, table):
        command = f'''
        DROP TABLE IF EXISTS {table};
        '''
        self.execute(command)

    def delete_column(self, table, column):
        command = f'''
        ALTER TABLE {table}
        DROP COLUMN {column};
        '''
        self.execute(command)

    def delete_cell(self, table, column, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        if column_filter[:5]=='__i__':
            column_filter = column_filter[5:]
        else:
            column_filter_value = f"'{column_filter_value}'"
        command = f'''
        UPDATE {table}
        SET {column} = NULL
        WHERE {column_filter} = {column_filter_value};
        '''
        self.execute(command)

    def delete_cells_in_column(self, table, column):
        command = f'''
        UPDATE {table}
        SET {column} = NULL
        '''
        self.execute(command)

    def delete_string(self, table, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        if column_filter[:5]=='__i__':
            column_filter = column_filter[5:]
        else:
            column_filter_value = f"'{column_filter_value}'"
        command = f'''
        DELETE FROM {table}
        WHERE {column_filter} = {column_filter_value};
        '''
        self.execute(command)

    def delete_all_strings(self, table):
        command = f'''
        DELETE FROM {table};
        '''
        self.execute(command)

    def get_tables(self):
        command = f'''
        SELECT name FROM sqlite_master where type='table';
        '''
        return self.execute(command)

    def get_columns_name(self, table):
        command = f'''
        SELECT name
        FROM PRAGMA_TABLE_INFO('{table}');
        '''
        return self.execute(command)

    def get_column_type(self, table, column):
        command = f'''
        SELECT type
        FROM PRAGMA_TABLE_INFO('{table}')
        WHERE name = '{column}';
        '''
        return self.execute(command)

    def get_columns_type(self, table):
        command = f'''
        SELECT type
        FROM PRAGMA_TABLE_INFO('{table}');
        '''
        return self.execute(command)

    def get_all_data(self, table):
        command = f'''
        SELECT *
        FROM {table}
        '''
        return self.execute(command)

    def get_columns_data(self, table, *columns):
        if len(columns)==0: raise ValueError('Not enough input.')
        if len(columns)==1: columns = str(columns)[1:-2]
        else: columns = str(columns)[1:-1]
        columns = columns.replace("'", '')
        command = f'''
        SELECT {columns}
        FROM {table};
        '''
        return self.execute(command)

    def get_all_data_filter(self, table, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        if column_filter[:5]=='__i__':
            column_filter = column_filter[5:]
        else:
            column_filter_value = f"'{column_filter_value}'"
        command = f'''
        SELECT *
        FROM {table}
        WHERE {column_filter} = {column_filter_value};
        '''
        return self.execute(command)

    def get_columns_data_filter(self, table, *columns, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        if len(columns)==0: raise ValueError('Not enough input.')
        if len(columns)==1: columns = str(columns)[1:-2]
        else: columns = str(columns)[1:-1]
        columns = columns.replace("'", '')
        command = f'''
        SELECT {columns}
        FROM {table}
        WHERE {column_filter} = '{column_filter_value}';
        '''
        return self.execute(command)


    def __str__(self):
        return self.path
    def __iter__(self):
        return self.get_tables()
    def inf(self):
        return {'name': self.path, 'tables': conv_matrix_to_list(conv_list(self.get_tables()))}
    def table(self, table):
        return Table(self.path, table)

class Table:
    def __init__(self, path, table):
        self.cursor = sqlite3.connect(path)
        self.path = path
        self.table = table

    def execute(self, command, *args):
        '''Method for execute commands
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        with self.cursor:
            return self.cursor.execute(command, args)

    def create_table(self, *columns):
        if len(columns) == 0: raise ValueError('Insufficient data. At least one column must be specified.')
        if len(columns) == 1: columns = (str(columns)[:-2]+')')
        command = f'''
        CREATE TABLE IF NOT EXISTS "{self.table}" {columns};
        '''
        self.execute(command)

    def add_column(self, *columns_without_type, **columns_type):
        if len(columns_type) == 0 and len(columns_without_type) == 0: raise ValueError('Insufficient data. At least one column must be specified.')
        if len(columns_type) == 1: columns_type = (str(columns_type)[:-2]+')')
        columns_type = columns_type | {column: '' for column in columns_without_type}
        commands = [f'''ALTER TABLE {self.table} ADD COLUMN {column} {columns_type[column]};''' for column in columns_type]
        for command in commands:
            self.execute(command)

    def add_string(self, **string_of_column):
        if len(string_of_column) == 0: raise ValueError('Insufficient data. At least one column-line must be specified.')
        command = f'''
        INSERT OR IGNORE INTO {self.table} ({str([column for column in string_of_column])[1:-1].replace("'", '')})
        VALUES ({str([string_of_column[column] for column in string_of_column])[1:-1]})
        '''
        self.execute(command)

    def rename_table(self, new_name):
        command = f'''
        ALTER TABLE {self.table}
        RENAME TO {new_name};
        '''
        self.execute(command)
        self.table = new_name

    def rename_column(self, old_name, new_name):
        command = f'''
        ALTER TABLE {self.table}
        RENAME COLUMN {old_name} TO {new_name};
        '''
        self.execute(command)

    def rename_cell(self, column='', value='', column_filter='', column_filter_value='', **kwargs):
        '''first the column with the new value, then the filter'''
        if not column and not value and not column_filter and not column_filter_value and len(kwargs)<2: raise ValueError('Not enough input. You need to specify the column name, new value, which column to filter on and the filter value.')
        if bool(column) != bool(value) or bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify two parameters at once, you can\'t just one.')
        if not column and len(kwargs)==0 or column and len(kwargs)==0: raise ValueError('Not enough input.')
        if len(kwargs)>2: raise ValueError('Insufficient data. It is too many values.')
        if len(kwargs)==1 and column:
            column_filter = next(iter(kwargs))
            column_filter_value = kwargs[next(iter(kwargs))]
        elif len(kwargs)==1 and not column:
            column = next(iter(kwargs))
            value = kwargs[next(iter(kwargs))]
        elif len(kwargs)==2:
            kws = [(column, kwargs[column]) for column in kwargs]
            column=kws[0][0]
            value=kws[0][1]
            column_filter=kws[1][0]
            column_filter_value=kws[1][1]
        command = f'''
        UPDATE {self.table}
        SET {column} = "{value}"
        WHERE {column_filter} = "{column_filter_value}"
        '''
        self.execute(command)

    def delete_table(self):
        command = f'''
        DROP TABLE IF EXISTS {self.table};
        '''
        self.execute(command)

    def delete_column(self, column):
        command = f'''
        ALTER TABLE {self.table}
        DROP COLUMN {column};
        '''
        self.execute(command)

    def delete_cell(self, column, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        command = f'''
        UPDATE {self.table}
        SET {column} = NULL
        WHERE {column_filter} = "{column_filter_value}";
        '''
        self.execute(command)

    def delete_cells_in_column(self, column):
        command = f'''
        UPDATE {self.table}
        SET {column} = NULL
        '''
        self.execute(command)

    def delete_string(self, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        command = f'''
        DELETE FROM {self.table}
        WHERE {column_filter} = '{column_filter_value}';
        '''
        self.execute(command)

    def delete_all_strings(self):
        command = f'''
        DELETE FROM {self.table};
        '''
        self.execute(command)

    def get_columns_name(self):
        command = f'''
        SELECT name
        FROM PRAGMA_TABLE_INFO('{self.table}');
        '''
        return self.execute(command)

    def get_column_type(self, column):
        command = f'''
        SELECT type
        FROM PRAGMA_TABLE_INFO('{self.table}')
        WHERE name = '{column}';
        '''
        return self.execute(command)

    def get_columns_type(self):
        command = f'''
        SELECT type
        FROM PRAGMA_TABLE_INFO('{self.table}');
        '''
        return self.execute(command)

    def get_all_data(self):
        command = f'''
        SELECT *
        FROM {self.table}
        '''
        return self.execute(command)

    def get_columns_data(self, *columns):
        if len(columns)==0: raise ValueError('Not enough input.')
        if len(columns)==1: columns = str(columns)[1:-2]
        else: columns = str(columns)[1:-1]
        columns = columns.replace("'", '')
        command = f'''
        SELECT {columns}
        FROM {self.table};
        '''
        return self.execute(command)

    def get_all_data_filter(self, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        command = f'''
        SELECT *
        FROM {self.table}
        WHERE {column_filter} = '{column_filter_value}';
        '''
        return self.execute(command)

    def get_columns_data_filter(self, *columns, column_filter='', column_filter_value='', **column_filter_kw):
        if bool(column_filter) != bool(column_filter_value): raise ValueError('Insufficient data. You need to specify parameter at once, you can\'t just one.')
        if not column_filter and not column_filter_value and len(column_filter_kw)==0: raise ValueError('Not enough input.')
        if column_filter and column_filter_value and len(column_filter_kw): raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==2: raise ValueError('Insufficient data. It is too many values.')
        if len(column_filter_kw)==1:
            column_filter = next(iter(column_filter_kw))
            column_filter_value = column_filter_kw[next(iter(column_filter_kw))]
        if len(columns)==0: raise ValueError('Not enough input.')
        if len(columns)==1: columns = str(columns)[1:-2]
        else: columns = str(columns)[1:-1]
        columns = columns.replace("'", '')
        command = f'''
        SELECT {columns}
        FROM {self.table}
        WHERE {column_filter} = '{column_filter_value}';
        '''
        return self.execute(command)

    def __str__(self):
        return self.table
    def __iter__(self):
        return self.get_columns_name()
    def inf(self):
        return {'name': self.table, 'columns': [{name: type} for name, type in zip(conv_matrix_to_list(conv_list(self.get_columns_name())), conv_matrix_to_list(conv_list(self.get_columns_type())))]}
    def database(self):
        return Database(self.path)

def conv_list(obj):
    to_return = [list(row) for row in obj.fetchall()]
    return to_return

def conv_matrix_to_list(obj):
    to_return = [value for list in obj for value in list]
    return to_return

def conv_tuple(obj):
    to_return = [tuple(row) for row in obj.fetchall()]
    return to_return

def conv_str(obj):
    to_return = conv_tuple(obj)
    if len(to_return)>1: raise ValueError('The object to be converted has more than one element. Use another conversion method')
    if len(to_return)==0: return None
    return to_return[0]

def conv_dict(obj):
    colname = [d[0] for d in obj.description]
    result_list = []
    to_return = {}
    strings = obj.fetchall()
    for r in strings:
        row = {}
        for col in range(len(colname)):
            row[colname[col]] = [r[col]]
        result_list.append(row)
        del row
    super_dict = defaultdict(list)
    for d in result_list:
        for k, v in d.items():
            super_dict[k] = list(super_dict[k] + v)
    for elem in super_dict.keys():
        to_return[elem] = super_dict[elem]

    return to_return


# db = Database('database.db')
# table1 = Table('database.db', 'Table1')
# print(conv_matrix_to_list(list(db.table('Table1'))))
# print(db)
# print(db.inf())
# print(list(table1))
# print(table1.inf())
# db.create_table('Table2', 'column1', 'column2')
# db.add_column('Table1', 'column1', column2='INTEGER', column3='INTEGER')
# db.add_string('Table2', column1='dsf', column2='234')
# db.rename_table('Table1', 'Table2')
# db.rename_column('Table1', 'column4', 'column5')
# db.rename_cell('Table1', 'column1', '25465', 'column2', '234')
# db.rename_cell('Table2', column1='25465', column2='234')
# db.delete_table('Table2')
# db.delete_column('Table1', 'column1')
# db.delete_cell('Table2', 'column1', column2='234')
# db.delete_cells_in_column('Table2', 'column1')
# db.delete_string('Table1', column2='234')
# print(conv_list(db.get_tables()))
# print(conv_tuple(db.get_tables()))
# print(conv_str(db.get_tables()))
# print(conv_list(db.get_columns_name('Table1')))
# print(conv_str(db.get_columns_type('Table1', 'column2')))
# print(conv_list(db.get_all_data('Table1')))
# print(conv_matrix_to_list(conv_list(db.get_all_data('Table1'))))
# print(conv_dict(db.get_all_data('Table1')))
# print(conv_dict(db.get_columns_data('Table1', 'column1')))
# print(conv_dict(db.get_columns_data('Table1', 'column1', 'column2')))
# db.get_all_data_filter('Table1', 'column1', '25465')
# db.get_all_data_filter('Table1', column2='234')
# print(conv_dict(db.get_columns_data_filter('Table1', 'column3', 'column4', column2='234')))
# db.add_string('users', user_id_out='555')
# db.add_string('tasks_common', user_id=db.get_)





# db.execute('''CREATE TABLE "embeds" (
# 	"id"	INTEGER,
# 	"user_id"	INTEGER,
# 	"title"	TEXT,
# 	"title_comment"	TEXT,
# 	"subtitle1"	TEXT,
# 	"subtitle1_comment"	TEXT,
# 	"subtitle2"	TEXT,
# 	"subtitle2_comment"	TEXT,
# 	"subtitle3"	TEXT,
# 	"subtitle3_comment"	TEXT,
# 	"thumbnail_image"	TEXT,
# 	"image"	TEXT,
# 	"footer"	TEXT,
# 	"color"	TEXT,
# 	"channel"	TEXT,
# 	PRIMARY KEY("id")
# );''')
# db.execute('''CREATE TABLE "messages" (
# 	"user_id"	INTEGER,
# 	"message1"	TEXT,
# 	"message2"	TEXT,
# 	"message3"	TEXT,
# 	"message4"	TEXT,
# 	"message5"	TEXT,
# 	PRIMARY KEY("user_id")
# );''')
# db.execute('''CREATE TABLE "plans" (
# 	"id"	INTEGER,
# 	"user_id"	INTEGER,
# 	"enable"	INTEGER DEFAULT 1,
# 	"for_time"	TEXT,
# 	"date"	TEXT,
# 	"text_up"	TEXT,
# 	"embed_id"	INTEGER,
# 	PRIMARY KEY("id"),
# 	FOREIGN KEY("embed_id") REFERENCES "embeds"("id")
# );''')

