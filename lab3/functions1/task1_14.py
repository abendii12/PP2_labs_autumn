#task1
def grams_to_ounces(grams):
    ounces = 28.3495231 * grams
    return ounces
print(grams_to_ounces())

#task2
def fahrenheit_to_centigrade(F):
    C = (5 / 9)*(F-32)
    return int(C)
print(fahrenheit_to_centigrade(454))

#task3
def solve(numheads, numlegs):
    for i in range(1, numheads+1):
        y = numheads - i
        if 2*i + 4*y == numlegs:
            print(f"{i} rabbits, {y} chickens")

solve(35, 94)

#task4
nums = input()
first_nums =list(map(int, nums.split()))
def is_prime(n):
    if n <=1:
        return False
    if n == 2:
        return True
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
        else:
            return True
        
def filter_prime(first_nums):
    return [number for number in first_nums if is_prime(number)]

prime = filter_prime(first_nums)
print("Prime numbers:", prime)

#task5
import itertools
def permut_word():
    word = input()
    permut = itertools.permutations(word)
    for perm in permut:
        print(''.join(perm))
        
permut_word()

#task6
def reversed_sent():
    user = input()
    sentence = user.split()
    rev = sentence[::-1]
    rev_sen = ' '.join(rev)
    print("Reversed sentence:", rev_sen)
reversed_sent()
    
#task7
def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i+1] == 3:
            return True
    return False
    
print(has_33([1, 2, 3, 3]))

#task8
def spy_game(nums):
    seq = [0, 0, 7]
    index = 0
    for num in nums:
        if num == seq[index]:
            index += 1
        if index == 3:  
            return True
    return False

print()  

#task9
import math
radius = int(input())
def volume_sph(rad):
    vol = (4/3)*math.pi * rad**3
    print(vol)
volume_sph(radius)
    
#task10
import math
radius = int(input())
def volume_sph(rad):
    vol = (4/3)*math.pi * rad**3
    print(vol)
volume_sph(radius)

#task11
def is_polindrome(string):
    string = string.lower().strip()
    if string == string[::-1]:
        return True  
    return False  

word = input()
print(is_polindrome(word))

"""
def is_polindrome(string):

    cleaned_string = ''.join(c.lower() for c in string if c.isalnum())
    left, right = 0, len(cleaned_string) - 1
    while left < right:
        if cleaned_string[left] != cleaned_string[right]:
            return False
        left += 1
        right -= 1
    return True
word = input()
print(is_polindrome(word))
"""

#task12
def histogram(lst):
    for number in lst:
        print('*' * number)
input_list = list(map(int, input().split()))

histogram(input_list)

#task13
import random

def guess_number():
    number_to_guess = random.randint(1, 20)
    name = input("Hello! What is your name? ")
    print(f"Well, {name}, I am thinking of a number between 1 and 20.")
    attempts = 0
    while True:
        guess = int(input("Take a guess: "))  
        attempts += 1
        
        if guess < number_to_guess:
            print("Your guess is too low.")
        elif guess > number_to_guess:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {attempts} guesses!")
            break  

guess_number()

#task14
from task1 import grams_to_ounces
from task2 import fahrenheit_to_centigrade
from task7 import has_33
from task8 import spy_game
#1 
grams_to_ounces(123)

#2
fahrenheit_to_centigrade(454)

#7
print(has_33([1, 3, 4, 5, 6, 3, 3]))

#8
print(spy_game([0, 0, 7, 1, 2, 8]))