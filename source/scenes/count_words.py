from collections import Counter
import os

c = Counter()

for filename in os.listdir('.'):
    if filename.endswith('scene.dry'):
        print(filename)
        text = ''
        with open(filename) as f:
            text = f.read()
        words = text.strip().split()
        words = [x.strip('.,*@:"?!><-=][()'  + "'").lower() for x in words]
        c.update(words)

print(c.most_common())
