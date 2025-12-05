
import os

def repeatword (min_repeat_count):
    word_count = {}

    with open("excersises/moby-dick.txt","r", encoding="utf-8") as file:
        contents = file.read()

    words = contents.split()
    for word in words: 
        word = word.lower()
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    repeats = {word: count for word, count in word_count.items() if count > min_repeat_count}

    sorted_repeats = sorted(repeats.items(), key=lambda item: [item[1]], reverse=False)

    print(f"Repeated words that appears at least {min_repeat_count} times: \n")
    for word, count in sorted_repeats:
        print(f"{word}: {count}")
    
    total_repeated_word = len(sorted_repeats)
    print(f"\nThe total number of unique words repeated at least {min_repeat_count} times: {total_repeated_word}")

repeatword(1000)




