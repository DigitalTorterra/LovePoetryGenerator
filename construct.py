from glob import glob

files = glob('./Text/**/*.txt',recursive=True)
files = [i for i in files if ('links.txt' not in i and 'poetry.txt' not in i)]

data = []
for file in files:
    with open(file,'r') as f:
        data.append(f.read())

with open('./Poet/poetry.txt','w') as f:
    for item in data:
        item = item.replace('We have the best collection of love poems on the web. Click here for more love poems on our site','')
        f.write(item)
        f.write('\s')
