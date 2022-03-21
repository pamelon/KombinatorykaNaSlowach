# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, too-many-instance-attributes, too-many-arguments

import argparse
from strategy import Basic

def begin_game():
    print("Cześć, witaj w grze w zmazywanie repetycji!")

    alf_length = int(input("Jak długi chcesz wybrać alfabet do rozgrywki?\n"))
    last_letter = chr(ord('A')+alf_length)
    print("W rozgrywce używaj dużych liter, bez polskich znaków, od A do {}".format(last_letter))

    word_length = int(input("Jak długie chcesz żeby bylo słowo dla zwycięstwa gracza 1?\n"))

    round_length = int(input("Ile rund chcesz żeby trwała rozgrywka?\n"))

    print("Gramy wielkimi literami A-{}, na słowo maksymalnej długości {}, na {} rund. \n"\
        .format(last_letter, word_length, round_length))

    return (alf_length, word_length, round_length)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-s', '--strategy', dest='strategy', type=int, default=0,
                        help='chosen strategy for the computer player')
    (alf_length, word_length, round_length) = begin_game()

    
main()