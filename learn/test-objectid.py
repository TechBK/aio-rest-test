from bson import objectid

a= objectid.ObjectId()
print(a)
print(str(a))

# print(a.str)

print(a.binary)