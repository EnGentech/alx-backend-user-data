class Check:
    id = 3
    name = "gentle"
    school = "ALX"

    def isn(self, key):
        if hasattr(self, key):
            print("valid")
        else:
            print("not found")

x = Check()
print(x.isn("nme"))