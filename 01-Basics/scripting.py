#print("HELLO WORLD")
#print(type([10, 20, 30]))
#print(type((1,2,3,4)))

#class Customer:
    #def identify(self,name):
        #print(f"I am Customer",name)

#cust = Customer()
#cust.identify("Laura")

numbers = [3,7,2,9,5,1]
largest = numbers[0]
for num in numbers:
    if num > largest:
        largest = num
print(f"Largest: {largest}")

n = 10
total = 0
for i in range(1, n + 1 ):
    total += i
print(f"Sum: {total}")

num1 = int(input("Enter the first number:"))
num2 = int(input("Enter the second number:"))

sum = num1 + num2
print(f"The sum of {num1} and {num2} is {sum}")
