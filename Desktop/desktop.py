import os, pathlib, json

json_dir = 'data.txt'
class Desktop():
    def __init__(self):
        with open(json_dir, 'r') as f:
            data = json.load(f)
        self.dir = [i.replace(' ', '') for i in data['dir']]
        self.types = data['types']
        print(self.dir)
    def build(self, dir, types):
        work = False
        dir.replace(" ", "")
        self.dir = dir.split(',')
        
        if len(self.dir) > 1:
            work = True
        self.types = types
        print('w')
        data = {
            'dir': self.dir,
            'types': types,
            'work': True,
            'downloads': work
        }
        with open(json_dir, 'w') as f:
            json.dump(data, f)
    def update(self):
        self.check_type()
    def check_type(self):
        # if work:
        #     for i in self.list:

        #         for key, values in self.types.items():
        #             for k in values:
        #                 print()
        #                 if pathlib.Path(str(i)).suffix == k:
        #                     File(self.dir, key, i)
        for directory in self.dir:
            for file in os.listdir(directory):
                for key, values in self.types.items():
                    for value in values:
                        if pathlib.Path(str(file)).suffix == value:
                            os.rename(f'{directory}/{file}', f'{self.dir[0]}/{key}/{file}')
                            print(f'{directory}/{file}', f'{self.dir[0]}/{key}/{file}')


