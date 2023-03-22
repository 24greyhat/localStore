from LocalStore import LocalStore

def func():
    print("Hello World!")

store = LocalStore("example", "123")

store.dump({"dict": {"key":"value"}})
store.dump({"tuple": (1,2,3,4)})
store.dump({"set": {1,2,3,4}})
store.dump({"array": [1,2,3,4]})

print(store.load())