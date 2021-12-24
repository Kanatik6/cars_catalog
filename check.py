a = '$ 12 200'
from decimal import Decimal as D
price = D(int(a.replace('$','').replace(' ','')))
print(price)