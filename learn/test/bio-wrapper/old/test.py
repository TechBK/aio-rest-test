def demo1():
    try:
        a = 0
        raise RuntimeError("To Force Issue")
    except:
        print('sdfkja')
        a = 1
        return 2
    # finally:
    #     return a
    a= 3
    return a
print(demo1())

if not {}:
    print('True')
else:
    print('False')