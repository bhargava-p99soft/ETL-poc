# # data = {
# #     name: "Tester",

# # }

# name, age, skills = "Tester", 25, ["dev", "testing"]


# # print(skills)

# def localVar(x):
#    print(x)
#    x = "developer"
#    print(x)
    

# localVar(name)

# print(f"{name} is in the global scope")


# from matplotlib import pyplot as plt
# import numpy as np

# # Generate 100 random data points along 3 dimensions
# x, y, scale = np.random.randn(3, 100)
# fig, ax = plt.subplots()

# # Map each onto a scatterplot we'll create with Matplotlib
# ax.scatter(x=x, y=y, c=scale, s=np.abs(scale)*500)
# ax.set(title="Some random data, created with JupyterLab!")
# plt.show()

class TestClass:
    pass

data = {
    "a": "key should be a",
    "b": {
        "c": "key should be b.c",
        "d": {
            "e": {
                "f": "key should be b.d.e.f"
            }
        }
    }
}

output = {
    'a': 'key should be a', 
    'b.c': 'key should be b.c', 
    'b.d.e.f': 'key should be b.d.e.f'
}


output = {}

def performRecursion(k, data):
    for i, v in enumerate(data):
        if(type(data[v]) is not dict):
            if(k != ""):
                output[k + "." + v] = data[v]
            else:
                output[v] = data[v]
        else:
            if(k != ""):
                performRecursion(k + "." + v, data[v])
            else:
                performRecursion(v, data[v])


dataStr = "hello"



performRecursion("", data)

print(output)
# print(dataStr[len(dataStr)::-1])


# for i in range(10):
#     print(i)