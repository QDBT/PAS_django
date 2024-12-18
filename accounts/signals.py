from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from system_main.models import File
from homepage.models import Project

@receiver(post_save, sender=User)
def create_initial_file(sender, instance, created, **kwargs):
    if created:
        # Training code for the initial file
        TranningCode = """
import random

def guess_the_number_simulated():
    print("Welcome to 'Guess the Number'!")
    print("I'm thinking of a number between 1 and 100.")
    print("Can you guess it?")

    # Generate a random number between 1 and 100
    number_to_guess = random.randint(1, 100)
    attempts = 0
    guessed_correctly = False

    # Predefined list of guesses
    simulated_guesses = [10, 20, 50, 75, 60, 65, 63, number_to_guess]  # Include the correct number eventually

    for guess in simulated_guesses:
        attempts += 1
        print(f"Attempt {attempts}: Guessing {guess}...")

        # Check the guess
        if guess < number_to_guess:
            print("Too low!")
        elif guess > number_to_guess:
            print("Too high!")
        else:
            print(f"Congratulations! The number was {number_to_guess}. You guessed it in {attempts} attempts.")
            guessed_correctly = True
            break

    if not guessed_correctly:
        print("Oh no! The guesses ran out before finding the number.")
"""
        # Create a Project instance for the user if necessary
        project, project_created = Project.objects.get_or_create(
            user=instance,
            defaults={'title': 'TRAINING', 'language': 'py'}
        )
        # Create a File instance associated with the new Project
        File.objects.create(
            project=project,
            file_name='Hello.py',
            code=TranningCode
        )
    
    