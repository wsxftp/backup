import json

a = json.dumps('{aaaa:(bbb,ccc),aa:cc}')
print(a)
b = json.loads(a)
print(b)
