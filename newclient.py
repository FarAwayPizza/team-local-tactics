from socket import socket
import json
from rich import print
from rich.prompt import Prompt
from rich.table import Table
import pickle
from core import Match, Shape

def print_match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')

'''

def print_available_champs(champions):

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    print(available_champs)
    #HER
    '''

    

def chosingCaracter(navnListe):

    while True:
        championName = input("Choose a champion:").lower()

        if championName in navnListe:
            print("you have chosen" + championName)
            navnListe.remove(championName)
            return championName
            
        else: 
            print("That champion is not available")

def motta(socket):
 
    recieved = socket.recv(1024)  
    packet = recieved.decode()
    #print(packet)
    translated = json.loads(packet)
    print(translated)

    navnListe = [champ["name"] for champ in translated] 
    print(navnListe)

    champ1 = chosingCaracter(navnListe)
    champ2 = chosingCaracter(navnListe)

    champs = champ1 + " " + champ2
    sock.send(champs.encode())

    print(champs)

      

with socket()as sock:
 
    server_address = ("localhost", 5555)
    sock.connect(server_address)
    '''
    sentence = input("Melding: ")

    sock.send(sentence.encode())
    colour = sock.recv(1024).decode()


    print(f"From Server: {colour}")
    #sock.close()

    '''

    motta(sock)

    recieved = sock.recv(4096)  
    match = pickle.loads(recieved)

    print_match_summary(match)



 
        

        





    