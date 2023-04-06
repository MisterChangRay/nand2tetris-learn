def spamrun(fn):
    def sayspam(*args):
        print("spam,spam,spam")
        print(args[0], args[1])
        fn(*args)
    return sayspam

@spamrun
def useful(a,b):
    print(a*b)
   
if __name__ == "__main__":
    for i in range(5):
    	print(i)
    	i+=1