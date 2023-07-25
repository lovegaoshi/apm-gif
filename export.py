import json
import os

with open(os.path.join('gifs','README.md'), 'w') as f:
    f.write('# gifs\n')
    for folder in os.listdir('gifs'):
        try:
            with open(os.path.join('gifs', folder, 'data.json')) as g:
                data_list, data_dict = json.load(g)
                f.write(f'## {folder}\n\n')
                for data_str in data_list:
                    f.write(f'![{data_dict[data_str]}]({data_str})\n\n')
        except Exception as e:
            print(e)
            pass
