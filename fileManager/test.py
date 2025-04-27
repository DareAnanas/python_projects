arr = ['.py', '.vim', '.txt']

arr = sorted((f for f in arr ), key=lambda f: f, reverse=True)

print(arr)