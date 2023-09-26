"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    count = 0
    for string_par in paragraphs :
        if select(string_par):
            count += 1
        if count == k + 1:
            return string_par
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def helper(list_sub):
        list_sub = remove_punctuation(list_sub)
        list_sub = lower(list_sub)
        list_sub = split(list_sub)
        return list_sub
    
    def select(paragraphs):
        paragraphs = helper(paragraphs)
        for word_a in topic:
            for word_b in paragraphs:
                if word_a == word_b:
                    return True
        return False
    return select

    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if typed_words == [] or reference_words == []:
        return 0.0
    else:
        count_words = 0
        right_words = 0
        len_ref = len(reference_words)
        for element in typed_words:
            if count_words <= len_ref-1:
                if element == reference_words[count_words]:
                    right_words += 1
            count_words += 1    
        return (right_words/count_words)*100.0
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    len_words = 0
    for i in typed:
        len_words += 1
    return len_words / 5 * 60 / elapsed
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    a = [0 for i in range(len(valid_words))]
    limit_number = 0
    flag = 1
    for i in range(len(valid_words)) :
        a[i] = diff_function(user_word,valid_words[i],limit)
        if a[i] < a[limit_number]:
            limit_number = i
        if a[i] <= limit:
            flag = 0
        if user_word == valid_words[i]:
            return valid_words[i]
    if flag :
        return user_word
    else:
        return valid_words[limit_number]
    # END PROBLEM 5

def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def helper(start, goal, limit,count = 0):
        if count > limit:
            return count
        if not start or not goal:
            return abs(len(start)-len(goal))
        else:
            if start[0] != goal[0]:
                return helper(start[1:],goal[1:],limit,count+1) + 1
            else:
                return helper(start[1:],goal[1:],limit,count)
    return helper(start, goal, limit,count = 0)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if start == goal :
        return 0
    elif not goal or not start :
        return abs(len(start)-len(goal))
    elif limit < 0 :
        return 100000
    else:
        if start[0] == goal[0] :
            return pawssible_patches(start[1:],goal[1:],limit)
        else:
            add_diff = pawssible_patches(start,goal[1:],limit-1)
            remove_diff = pawssible_patches(start[1:],goal,limit-1)
            substitude_diff = pawssible_patches(start[1:],goal[1:],limit-1)
            return min(add_diff,remove_diff,substitude_diff) + 1


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    len_two = min(len(start),len(goal))
    if len_two >= 1:
        for i in range(len_two-1):
            if start[i] == goal[i+1] and goal[i] == start[i+1] :
                return 1

###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    len_size = len(prompt)
    index = 0
    for word in typed:
        if word == prompt[index]:
            index += 1
        else:
            break
    send({'id':user_id,'progress':index/len_size})
    return index/len_size
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    len_oppent = len(times_per_player)
    len_time = len(times_per_player[0])
    time_word = []
    for j in range(len_oppent):
        time_word += [[]]
        for i in range(len_time-1):
            time_word[j] += [times_per_player[j][i+1]-times_per_player[j][i]]
    return game(words,time_word)


    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    number_oppoent = len(all_times(game))
    number_words = len(all_words(game))
    fast = []
    for i in range(number_oppoent):
        fast += [[]]
    index = []
    for i in range(number_words):
        index += [0]
        for j in range(number_oppoent):
            if all_times(game)[j][i] < all_times(game)[index[i]][i]:
                index[i] = j
        print("DEBUG:",index[i])
    words = []
    for i in range(number_oppoent):
        words += [[]]
        for j in range(number_words):
            if index[j] == i:
                words[i] += [word_at(game, j)]
    return words
    

    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)