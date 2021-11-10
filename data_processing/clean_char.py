import csv
table_names = ['Characters', 'equip', 'Level_up', 'Loc_Materials', 'Locate', 'Materials', 'Nations', 'owning',
               'Talent_level_up_materials', 'Users', 'Weapons']
class get_query():
    def __init__(self, input_path, outout_path, table_name):
        self.input_path = input_path
        self.output_path = outout_path
        self.table_name = table_name
        self.rules_dict = {'Characters': [1, 2, 4, 5], 'Weapons': [1, 3, 5], 'Materials': [1],
                            'Talent_level_up_materials': [1], 'Users': [1, 5], 'Locate': [2]}
        if table_name != 'Users':
            encoding = 'utf-8'
        else:
            encoding = 'gbk'
        with open(self.input_path, encoding=encoding) as f:
            csv_reader = csv.reader(f)
            self.data = []
            if self.table_name in self.rules_dict:
                for line in csv_reader:
                    for i in self.rules_dict[self.table_name]:
                        line[i] = "'" + line[i] + "'"
                    print(line)
                    self.data.append(line)
            else:
                for line in csv_reader:
                    self.data.append(line)
            f.close()


    def query_in_txt(self):
        n = len(self.data)
        print(n)
        with open(self.output_path, 'a') as f:
            prefix = 'insert into ' + self.table_name + ' values ('
            for i in range(1, n):
                mainpart = ",".join(self.data[i])
                query = prefix + mainpart + ');'
                print(query)
                f.write(query)
                f.write("\n")
            f.close()
input_folder = './part3/csv/'
output_folder = './part3/txt/'
input_paths = []
output_paths = []
name = 'equip'
input_paths.append(input_folder+name+'.csv')
output_paths.append(output_folder+name+'.txt')
test = get_query(input_paths[0], output_paths[0], name)
test.query_in_txt()
