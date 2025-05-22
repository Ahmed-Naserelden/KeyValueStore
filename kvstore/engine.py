import os
import sys
import json
from datetime import datetime

def read_json(file_path):
    data = []
    with open(file_path, 'r') as f:
        content = f.read()
        data = json.loads(content)
    return data

class KVEngine:

    def __init__(self):
        self.current_namespace = None
        self.STORE_PATH = os.path.join(os.path.dirname(__file__), 'store')
        self.LOG_PATH = os.path.join(self.STORE_PATH, 'log')
        self.LOG_FILE_PATH = os.path.join(self.LOG_PATH, 'log.log')

        if not os.path.exists(self.STORE_PATH):
            os.makedirs(self.STORE_PATH)
            print(f"Store path {self.STORE_PATH} created.")

        if not os.path.exists(self.LOG_PATH):
            os.makedirs(self.LOG_PATH)
            print(f"Log path {self.LOG_PATH} created.")

        self.write_log("KVEngine initialized.")
        
        self.NAMESPACE_PATH = None
        self.size = 0
        self.buffer = []

        self.buffer_dict = {}
        self.filtterd_buffer = {}

        self.MaxBuffer = 10

        print("KVEngine initialized.")
        print(f"Store path: {self.STORE_PATH}")
        print(f"Log path: {self.LOG_PATH}")

    def switch_namespace(self):
        self.NAMESPACE_PATH = os.path.join(self.STORE_PATH, self.current_namespace)

    def list_namespaces(self):
        """
        List all namespaces.
        """
        if not os.path.exists(self.STORE_PATH):
            return []
        namespaces = [name for name in os.listdir(self.STORE_PATH)
                        if os.path.isdir(os.path.join(self.STORE_PATH, name))]
        namespaces.remove('log')
        return namespaces    

    def create_namespace(self, namespace):
        """
        Create a new namespace.
        """
        os.makedirs(os.path.join(self.STORE_PATH, namespace), exist_ok=True)
        print(f"Namespace {namespace} created successfully.")

    def use_namespace(self, namespace):
        """
        Use a specific namespace.
        """
        self.current_namespace = namespace
        self.switch_namespace()

    def delete_namespace(self, namespace):
        """
        Delete a namespace.
        """
        namespace_path = os.path.join(self.STORE_PATH, namespace)
        if os.path.exists(namespace_path):
            os.rmdir(namespace_path)
    
    def namespace_exists(self, namespace):
        """
        Check if a namespace exists.
        """
        namespace_exists = os.path.exists(os.path.join(self.STORE_PATH, namespace))
        return namespace_exists
    
    def list_tables(self, namespace):
        namespace_dir=os.path.join(self.STORE_PATH, namespace)          
        return os.listdir(namespace_dir)
    
    def table_exists(self, namespace, table):
        table_path=os.path.join(self.STORE_PATH, namespace, table)
        return os.path.exists(table_path)



    def create_table(self, namespace, table):
        table_path=os.path.join(self.STORE_PATH, namespace, table)
        os.makedirs(table_path)

    def delete_table(self, namespace, table):
        """
        Delete a table in a namespace.
        """
        table_path = os.path.join(self.STORE_PATH, namespace, table)
        os.rmdir(table_path)
        pass

    def set_key(self, table, key, value , ttl=None):
        print('*' * 50)
        print(self.buffer)
        print('*' * 50)
        self.buffer.append({table: {key: {"value": value, "ttl": ttl}}})    
        self.size += 1
        print(self.buffer)
        if self.size >= self.MaxBuffer:
            self.flush_buffer(table)
            self.size = 0
        return True

    def get_key(self, table, key):
        bl = self.buffer
        bl.reverse()
        for item in bl:
            if table in item and key in item[table]:
                value = item[table][key]
                return value
        table_path = os.path.join(self.STORE_PATH, self.current_namespace, table)
        list_files = os.listdir(table_path)
        list_files.reverse()
        for filename in list_files:
            file_path = os.path.join(table_path, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
                if key in data:
                    return data[key]
        return None

    def delete_key(self, table, key):
        """
        Delete a key-value pair from a table.
        """
        value = {table: {key: {}}}
        self.buffer.append(value)
        # or
        deleted_key = {table: {key: {}}}
        self.buffer.append(deleted_key)

    def flush_table(self, table):
        """
        Flush a specific table.
        """
        self.convert_buffer_to_dict()
        self.get_filtterd_buffer()
        self.write_file()
        self.buffer = []
        self.buffer_dict = {}
        self.filtterd_buffer = {}
        pass

    def compact_table(self, table):
        """
        Compact a specific table.
        """

        table_path = os.path.join(self.STORE_PATH, self.current_namespace, table)
        list_files = os.listdir(table_path)
        list_files = sorted(list_files)
        
        files = []
        for _file in list_files:
            file_path = os.path.join(table_path, _file)
            new_file_path = os.path.join(table_path, f"{table}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
            d = read_json(file_path)
            files.append(d)

        compact_dict = dict()

        for file in files:
            for record_key in file.keys():
                record_value= file[record_key]
                if record_key in compact_dict:
                    if compact_dict[record_key]['ttl'] < record_value['ttl']:
                        compact_dict[record_key] = file[record_key]
                else:
                    compact_dict[record_key] = file[record_key]

        with open(new_file_path, 'w') as f:
            json.dump(compact_dict, f, indent=4)

        for file in list_files:
            file_path = os.path.join(table_path, file)
            os.remove(file_path)

    def get_name(self):
        return self.current_namespace
    
    def write_log(self, data):
        if not os.path.exists(self.LOG_FILE_PATH):
            with open(self.LOG_FILE_PATH, 'w') as log_file:
                log_file.write('')
        with open(self.LOG_FILE_PATH, 'a') as log_file:
            log_file.write(data + '\n')

    def create_log(self, data, action, namespace=None, table=None, key=None):
        log_entry = f'[{action}] {data} | {namespace} | {table} | {key}'
        return log_entry
    
    def convert_buffer_to_dict(self):
        buffer_dict = {}
        for entry in self.buffer:
            for table, data in entry.items():
                if table not in buffer_dict:
                    buffer_dict[table] = {}
                for row, values in data.items():
                    if row not in buffer_dict[table]:
                        buffer_dict[table][row] = []
                    buffer_dict[table][row].append(values)
        self.buffer_dict = buffer_dict
    
    def get_filtterd_buffer(self):
        filtered_buffer = {}                    
        for table_name, table_data in self.buffer_dict.items():
            filtered_buffer[table_name] = {}
            for row_key, row_data_list in table_data.items():
                for row_data in row_data_list:
                    filtered_buffer[table_name][row_key] = row_data
        self.filtterd_buffer = filtered_buffer

    def write_file(self):
        for table, rows in self.filtterd_buffer.items():
            table_path = os.path.join(self.NAMESPACE_PATH, table)
            file_path = os.path.join(table_path, f"{table}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
            with open(file_path, 'w') as f:
                json.dump(rows, f, indent=4)


if __name__ == "__main__":
    kv = KVEngine()