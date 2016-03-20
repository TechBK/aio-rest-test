import swiftclient  # $ sudo pip3 install python-swiftclient

user = 'admin'
key = 'baogavn'
tenant = 'admin'
authurl = 'http://192.168.145.132:5000/v2.0'

conn = swiftclient.client.Connection(
    user=user,
    tenant_name=tenant,
    auth_version='2.0',
    key=key,
    authurl=authurl
)

container_name = 'sdfasfsadfas'
# conn.put_container(container_name)

# with open('hello.txt', 'r') as hello_file:
#     conn.put_object(container_name, 'hello.txt',
#                     contents=hello_file.read(),
#                     content_type='text/plain')

print(conn.head_container(container_name))
print("next", conn.get_container(container_name))
#
# for container in conn.get_account()[1]:
#     print(container['name'])
#
# for data in conn.get_container(container_name)[1]:
#     print('{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified']))
#
#
# obj_tuple = conn.get_object(container_name, 'hello.txt')
# print(obj_tuple[0], obj_tuple[1])
# with open('my_hello.txt', 'wb') as my_hello:
#     my_hello.write(obj_tuple[1])

