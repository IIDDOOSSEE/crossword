import random
from django.shortcuts import render
from wordbank.models import wordBank

def get_words_with_shared_letters(all_words, num_words=5):
    selected_words = []
    while len(selected_words) < num_words:
        # เลือกคำใหม่
        new_word = random.choice(all_words)
        
        # เช็คว่ามีตัวอักษรซ้ำกับคำที่เลือกแล้วหรือไม่
        if not selected_words:
            selected_words.append(new_word)
        else:
            can_add = False
            for word in selected_words:
                # หาอักษรที่ซ้ำระหว่างคำ
                common_letters = set(new_word.word).intersection(set(word.word))
                if common_letters:
                    can_add = True
                    break
            if can_add:
                selected_words.append(new_word)
    return selected_words

def puzzle(request):
    all_words = list(wordBank.objects.all())

    # สุ่มเลือกคำที่มีตัวอักษรซ้ำกัน
    selected_words = get_words_with_shared_letters(all_words, num_words=5)

    return render(request, "crossword/puzzle.html", {"words": selected_words})
