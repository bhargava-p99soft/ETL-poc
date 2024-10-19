fruits = ["apples", "bananas"]

fruits.append("cinnamon")

print(fruits)

myFruits = fruits.copy()

print(myFruits == fruits)

myFruits.extend("hello")

# print(myFruits)
print(myFruits.reverse())


# try:
#     # comment: 
#     print(myFruits.index(5))
# except Exception as e:
#     print(e)
# # end try

print(dir(myFruits))