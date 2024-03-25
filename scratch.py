

def outer():
    def inner():
        print('Something is happening before the function')
        func()
        print('Something is happening after the function')
    return inner

def jump():
    print('I am jumping')

def swim():
    print('I am swimming')

    # jump = decorator(jump)
jump()

# swim = decorator(swim)
swim()