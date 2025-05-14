class test:
    def __call__(self, a, b):
        return (a + b)
        
print(test()(1, 2))