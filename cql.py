import os

def unsafe_eval(user_input):
    result = eval(user_input)
    return result

def main():
    user_input = input("Enter a mathematical expression: ")
    result = unsafe_eval(user_input)
    print("Result:", result)

if __name__ == "__main__":
    main()
