def get_computer_choice(user_choice):
    # Simple algorithm: if user chooses rock, computer chooses paper; if user chooses paper, computer chooses scissors; if user chooses scissors, computer chooses rock.
    if user_choice == "rock":
        return "paper"
    elif user_choice == "paper":
        return "scissors"
    elif user_choice == "scissors":
        return "rock"

def get_user_choice():
    choice = input("Enter your choice (rock, paper, scissors): ").lower()
    while choice not in ["rock", "paper", "scissors"]:
        choice = input("Invalid choice. Please enter rock, paper, or scissors: ").lower()
    return choice

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "You win!"
    else:
        return "Computer wins!"

def play_game():
    while True:
        user_choice = get_user_choice()
        computer_choice = get_computer_choice(user_choice)
        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")
        print(determine_winner(user_choice, computer_choice))
        
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()