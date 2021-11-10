import csv
class get_query():
    def __init__(self, input_path, outout_path, table_name):
        self.input_path = input_path
        self.output_path = outout_path
        self.table_name = table_name
        if table_name != 'Users':
            encoding = 'utf-8'
        else:
            encoding = 'gbk'
        with open(self.input_path, encoding=encoding) as f:
            csv_reader = csv.reader(f)
            self.data = []
            for line in csv_reader:
                self.data.append(line)
            f.close()


    def query_in_txt(self):
        n = len(self.data)
        with open(self.output_path, 'a') as f:
            prefix = 'insert into ' + self.table_name + ' values ('
            for i in range(1, n):
                mainpart = ",".join(self.data[i])
                query = prefix + mainpart + ');'
                print(query)
                f.write(query)
                f.write("\n")
            f.close()

input_folder = './part2/csv/'
output_folder = './part2/txt/'
table_names = ['Characters', 'equip', 'Level_up', 'Local_Materials', 'Locate', 'Materials', 'Nations', 'owning',
               'Talent_level_up_materials', 'Users', 'Weapons']
input_paths = []
output_paths = []
for name in table_names:
    input_paths.append(input_folder+name+'.csv')
    output_paths.append(output_folder+name+'.txt')
for i in range(11):
    test = get_query(input_paths[i], output_paths[i], table_names[i])
    test.query_in_txt()