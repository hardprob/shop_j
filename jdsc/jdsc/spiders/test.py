import time
a='https://list.jd.com/list.html?cat=9987%2C653%2C655&page=1&s=27&click=0'
b='https://list.jd.com/listNew.php?cat=9987%2C653%2C655&page=2&s=27&scrolling=y&log_id=1652010973841.8691&tpl=3_M&isList=1&show_items='
print(len(a))
print(len(b))
print(2%2==1)
print(time.time()*1000)

b=[('9987', '830', '862')]
c=list(b[0])
c.append(str(1))

print(c)
