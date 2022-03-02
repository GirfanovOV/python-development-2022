import textdistance as td
import random

def bullscows(guess: str, secret: str) -> tuple[int, int] :
    return (td.hamming.similarity(guess, secret), int(td.sorensen(guess, secret) * len(guess)))

def gameplay(ask: callable, inform: callable, words: list[str]) -> int :
    secret : str = random.choice(words)
    attempts =  0
    ask.word_len = len(words[0])
    while 1 :
        attempts += 1
        guess : str = ask("Введите слово: ", words)
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        if guess == secret :
            break
    return attempts
    

def ask(prompt: str = '', valid: list[str] = None) -> str :

    guess = ''
    while 1 : 
        guess = input(prompt)
        if len(guess) == ask.word_len and (not(valid) or (guess in valid)) :
            break

    return guess

def inform(format_string: str, bulls: int, cows: int) -> None :
    print(format_string.format(bulls, cows))
    
