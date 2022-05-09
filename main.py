# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, too-many-instance-attributes, too-many-arguments

import argparse
from strategy import Basic
from math import ceil

def begin_game(strategy):
    print("Cześć, witaj w grze w zmazywanie repetycji!")

    alf_length = int(input("Jak długi chcesz wybrać alfabet do rozgrywki?\n"))
    last_letter = chr(ord('A')+alf_length-1)
    print("W rozgrywce używaj dużych liter, bez polskich znaków, od A do {}".format(last_letter))

    word_length = int(input("Jak długie chcesz żeby bylo słowo dla zwycięstwa gracza 1?\n"))

    round_length = int(input("Ile rund chcesz żeby trwała rozgrywka?\n"))

    print("Gramy wielkimi literami A-{}, na słowo maksymalnej długości {}, na {} rund. \n"\
        .format(last_letter, word_length, round_length))

    return run_game(alf_length, word_length, round_length)

def check_for_repetitions(word):
    reversed_word = word[::-1]
    for i in range(1, int(ceil(len(word)/2)+1)):
        if reversed_word[:i] == reversed_word[i:2*i]:
            return reversed_word[2*i:][::-1],True
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


def pc_strategy(word, word_length, alf):
    word += alf[0]
    return word


def pc_turn(word, word_length, alf):
    word = pc_strategy(word, word_length, alf)
    new_word, changed = check_for_repetitions(word)
    if changed:
        print(f"PC {word} -> {new_word}")
    else:
        print(f"PC {word}")
    return new_word


#True - wygraliśmy my, False - wygrał komputer
def run_game(alf_length, word_length, round_length):
    alf = [chr(ord('A')+i) for i in range(alf_length)]
    print(alf)
    outcome = True

    word = ''
    for i in range(round_length):
        word = pc_turn(word, word_length, alf)
        if len(word) >= word_length:
            outcome = False
        word = human_turn(word, alf)
        if word == 'q':
            return
        if len(word) >= word_length:
            outcome = False
    return outcome


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-s', '--strategy', dest='strategy', type=int, default=0,
                        help='chosen strategy for the computer player')
    args = vars(parser.parse_args())

    result = begin_game(args['strategy'])

    if(result):
        print("Brawo wygrałaś!")
    else:
        print("Wygrał przeciwnik. Następnym razem na pewno pójdzie Ci lepiej :)")


main()
