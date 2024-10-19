
# import inspect module 
import inspect 
  
# our treeClass function 
def treeClass(cls, ind = 0): 
    
      # print name of the class 
    print (' -' * ind, cls.__name__) 
      
    # iterating through subclasses 
    for i in cls.__subclasses__(): 
        treeClass(i, ind + 3) 
  
print("Hierarchy for Built-in exceptions is : ") 
  
# inspect.getmro() Return a tuple  
# of class  cls’s base classes. 
  
# building a tree hierarchy  
inspect.getclasstree(inspect.getmro(BaseException)) 
  
# function call 
treeClass(BaseException) 
