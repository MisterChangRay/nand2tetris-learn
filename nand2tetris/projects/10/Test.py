def spamrun(fn):
    def sayspam(*args):
        print("spam,spam,spam")
        fn(*args)
    return sayspam
@spamrun
def useful(a,b):
    print(a*b)
   
if __name__ == "__main__"
    useful(2,5) 