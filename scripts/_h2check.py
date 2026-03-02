import re
with open(r'D:\dev\projects\protrainerprep\src\data\post\youth-fitness-certification.mdx', encoding='utf-8') as f:
    t = f.read()
h = re.findall(r'^\s*##\s+(.+)', t, re.M)
print(f'{len(h)} H2s: {h}')
