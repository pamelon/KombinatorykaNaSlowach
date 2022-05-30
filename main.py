# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, too-many-instance-attributes, too-many-arguments

import argparse
from math import ceil
from random import randint

def begin_game(strategy):
    print("Cześć, witaj w grze w zmazywanie repetycji!")

    alf_length = int(input("Jak długi chcesz wybrać alfabet do rozgrywki?\n"))
    last_letter = chr(ord('A')+alf_length-1)
    print("W rozgrywce używaj dużych liter, bez polskich znaków, od A do {}".format(last_letter))

    word_length = int(input("Jak długie chcesz żeby bylo słowo dla zwycięstwa gracza 1?\n"))

    round_length = int(input("Ile rund chcesz żeby trwała rozgrywka?\n"))

    print("Gramy wielkimi literami A-{}, na słowo maksymalnej długości {}, na {} rund. \n"\
        .format(last_letter, word_length, round_length))

    return run_game(alf_length, word_length, round_length, strategy)

def check_for_repetitions(word):
    reversed_word = word[::-1]
    for i in range(1, int(ceil(len(word)/2)+1)):
        if reversed_word[:i] == reversed_word[i:2*i]:
            return reversed_word[i:][::-1],True
    return word, False

def human_turn(word, alf):
    new_letter = None
    while new_letter is None:
        print(f"Czlowiek : {word}", end='')
        new_letter = input()
        if len(new_letter) != 1:
            print("\n Prosze dodac pojedyncza litere")
            new_letter = None
        elif new_letter == 'q':
            return new_letter
        elif new_letter not in alf:
            print(f"\n Prosze podac litere z alfabetu : {alf}")
            new_letter = None
        else:
            word += new_letter
            new_word, changed = check_for_repetitions(word)
            if changed:
                print(f"Czlowiek : {word} -> {new_word}")
            return new_word

    return word

def pc_turn(word, word_length, alf, strategy):
    word = globals()[strategy](word, alf)
    new_word, changed = check_for_repetitions(word)
    if changed:
        print(f"PC {word} -> {new_word}")
    else:
        print(f"PC {word}")
    return new_word

#check if adding a new given letter will create a repetition
def check_for_repetitions_add_letter(word, letter):
    reversed_word = (word + letter)[::-1]
    for i in range(1, int(ceil(len(word)/2)+1)):
        if reversed_word[:i] == reversed_word[i:2*i]:
            return True
    return False

#we check if there are no repetitions, then we add the letter
#if all letters create a repetition, add the first letter
def pc_strategy_no_repetitions(word, alf):
    for letter in alf:
        if check_for_repetitions_add_letter(word, letter):
            continue
        else:
            word +=letter
            return word

    word += alf[0]
    return word

#dummy strategy for checking the game running
def pc_strategy_first_symbol(word, alf):
    word += alf[0]
    return word

#Take a word and never create repetitions of lenght less than 4.
def pc_strategy_article(word, alf):
    first_part_word = word[-3:]
    for letter in alf:
        if letter not in first_part_word:
            word += letter
            break
    return word

def pc_strategy_furthest(word, alf):
    #a letter has not appeared before, add it and return
    if len(list(set(list(word)))) < len(alf):
        for letter in alf:
            if letter not in word:
                word += letter
                return word

    #if all letters have appeared at some point, let's see which one is the furthest in the word
    #reversing the string in the for loop
    appeared = []
    for letter in word[::-1]:
        appeared.append(letter)
        appeared = list(set(list(appeared)))
        if len(appeared) == len(alf) -1:
            new_letter = list(set(alf) - set(appeared)) + list(set(alf) - set(appeared))
            #if this letter does not create a repetition
            if not check_for_repetitions_add_letter(word, new_letter[0]):
                word += new_letter[0]
                return word
            #we go from the last one, if the last letter creates a repetition
            #take the furthest one which does not create a repetiton
            for ap_letter in appeared:
                if not check_for_repetitions_add_letter(word, ap_letter):
                    word += ap_letter
                    return word

    #if all create a repetition, add the first one
    word += alf[0]
    return word

def pc_strategy_bigrams(word, alf):
    #a letter has not appeared before, add it and return
    if len(list(set(list(word)))) < len(alf):
        for letter in alf:
            if letter not in word:
                word += letter
                return word

    #if all letters have appeared at some point, let's see if we can not create a bigram in the next turn
    #reversing the string in the for loop
    appeared_after = []
    last_letter = word[-1]
    for i in range(len(word)-1):
        if word[i] == last_letter:
            appeared_after.append(word[i+1])
    #if bigram will happen anyway, lets add a random letter
    if len(appeared_after) >= len(alf) -1:
        random_number = randint(0, len(alf) -1)
        word += alf[random_number]
        return word

    no_bigram_letters = list(set(alf) - set(appeared_after)) + list(set(alf) - set(appeared_after))
    #we go through all the letters that does not create bigrams
    #take the one which does not create a repetiton if possible
    for no_bi_letter in no_bigram_letters:
        if not check_for_repetitions_add_letter(word, no_bi_letter):
            word += no_bi_letter
            return word
    
    #if all create a repetition, add the first one
    word += alf[0]
    return word

#True - wygraliśmy my, False - wygrał komputer
def run_game(alf_length, word_length, round_length, strategy):
    alf = [chr(ord('A')+i) for i in range(alf_length)]
    print(alf)
    outcome = True

    word = ''
    for i in range(round_length):
        word = pc_turn(word, word_length, alf, strategy)
        if len(word) >= word_length:
            outcome = False
            #we finish game if the word is long enough that we lose
            return outcome
        word = human_turn(word, alf)
        if word == 'q':
            return
        if len(word) >= word_length:
            outcome = False
            #we finish game if the word is long enough that we lose
            return outcome
    return outcome

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-s', '--strategy', dest='strategy', choices=('pc_strategy_first_symbol', 'pc_strategy_article', 'pc_strategy_furthest', 'pc_strategy_bigrams', 'pc_strategy_no_repetitions'),
                        default='pc_strategy_article', help='chosen strategy for the computer player')
    args = vars(parser.parse_args())

    result = begin_game(args['strategy'])

    if(result):
        print("Brawo wygrałaś!")
    else:
        print("Wygrał przeciwnik. Następnym razem na pewno pójdzie Ci lepiej :)")


main()
