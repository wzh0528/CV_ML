import six
a='82386/243/7246'
b='60947//7245'
print(six.ensure_str(a).split('/'))
for index in six.ensure_str(a).split('/'):
    if not index:
        continue
    print(index)