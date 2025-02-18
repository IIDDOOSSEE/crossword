# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from wordbank.models import wordBank
from user.models import Account
from hangman.models import fail_count
import json


import random
def index(request):
    return render(request,"hangman/index.html");
def get_new_word():
    try:
        # Get both word and meaning
        word_objects = list(wordBank.objects.values('word', 'meaning'))
        if not word_objects:
            return {"word": "HANGMAN", "meaning": "A guessing game"}
        
        word_object = random.choice(word_objects)
        return {
            "word": word_object['word'].upper(),
            "meaning": word_object['meaning']
        }
    except Exception as e:
        print(f"Error getting word from database: {e}")
        return {"word": "HANGMAN", "meaning": "A guessing game"}

def initialize_session(request):
    """Initialize or reset game session data"""
    word_data = get_new_word()
    request.session['word'] = word_data['word']
    request.session['meaning'] = word_data['meaning']
    request.session['guessed_letters'] = []
    request.session['attempts_left'] = 6
    request.session.modified = True

@require_http_methods(["GET"])
def hangman_game(request):
    if 'word' not in request.session:
        initialize_session(request)
    
    word = request.session.get('word', '')
    meaning = request.session.get('meaning', '')
    guessed_letters = request.session.get('guessed_letters', [])
    attempts_left = request.session.get('attempts_left', 6)
    
    # แยกตัวอักษรที่ถูกต้องและผิดออกจากกัน
    correct_letters = [letter for letter in guessed_letters if letter in word]
    incorrect_letters = [letter for letter in guessed_letters if letter not in word]
    
    # Create display word with guessed letters
    display_word = ''.join([letter if letter in guessed_letters else '_' for letter in word])
    
    game_won = '_' not in display_word
    game_over = attempts_left <= 0
    
    context = {
        'display_word': ' '.join(display_word),  # Add spaces between letters
        'meaning': meaning,  # Add meaning to context
        'guessed_letters': sorted(guessed_letters),
        'incorrect_letters': incorrect_letters,  # ส่งข้อมูลตัวอักษรที่ผิด
        'attempts_left': attempts_left,
        'game_won': game_won,
        'game_over': game_over,
        'word': word 
    }
    
    return render(request, 'hangman/game.html', context)


@require_http_methods(["POST"])
def guess_letter(request):
    if 'word' not in request.session:
        initialize_session(request)
        return redirect('hangman:hangman_game')
    
    letter = request.POST.get('letter', '').upper()
    
    if letter and letter.isalpha() and len(letter) == 1 and letter.isascii():
        guessed_letters = request.session.get('guessed_letters', [])
        
        if letter not in guessed_letters:
            guessed_letters.append(letter)
            request.session['guessed_letters'] = guessed_letters
            
            if letter not in request.session['word']:
                request.session['attempts_left'] = request.session.get('attempts_left', 6) - 1
            # บอกจังโก้ว่า sesstion ถูกแก้ไขนะ 
            request.session.modified = True 
        else:
            messages.warning(request, 'You already guessed that letter!')
    else:
        messages.error(request, 'Please enter a valid single letter!')
    
    return redirect('hangman:hangman_game')

@require_http_methods(["POST"])
def reset_game(request):
    initialize_session(request)
    messages.info(request, 'New game started!')
    return redirect('hangman:hangman_game')

def save_fail_count(request):
    if request.method == 'POST':
        # รับข้อมูลจาก body request
        data = json.loads(request.body)
        username = data.get('username')
        word = ''.join(data.get('word').split(" ")).lower()
        print(word)
        fails = data.get('fails')
        
        try:
            user = Account.objects.get(username=username)
            word_obj = wordBank.objects.get(word=word)
            
            # เก็บข้อมูลในตาราง fail_count
            fail_entry, created = fail_count.objects.update_or_create(
                username=user,
                word=word_obj,
                defaults={'fails': fails}
            )
            
            return JsonResponse({'status': 'success', 'message': 'Data saved successfully.'})
        except Account.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found.'}, status=404)
        except wordBank.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Word not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)