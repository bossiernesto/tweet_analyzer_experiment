from .abstract import Persistance
import dataset


class DatasetPersistance(Persistance):
    def __init__(self, filename, default_table_name):
        super(DatasetPersistance, self).__init__(filename, None)
        self.connection = dataset.connect(filename)
        self.table_name = default_table_name

    def persist_header(self, data):
        pass

    def persist_data(self, data):
        pass

    def persist_to_table(self, table_name, data, function):
        if not callable(function):
            raise ("function is not callable on persist data")
        table = self.connection[table_name]
        function(table, data)
