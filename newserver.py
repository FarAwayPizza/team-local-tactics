from multiprocessing.sharedctypes import Value
from socket import socket
from struct import pack
from threading import Thread

from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team

import pickle
import json


def _parse_champ(champ_dict):

    name = champ_dict["name"]
    rock = champ_dict["probs1"]
    paper = champ_dict["probs2"]
    scissors = champ_dict["probs3"]
    
    return Champion(name, float(rock), float(paper), float(scissors))


def from_json() -> dict[str, Champion]:
    champions = {}
    with open("all_champs.json", 'r') as champfile:
        champsList = json.load(champfile)
        for champion in champsList:
            champ = _parse_champ(champion)
            champions[champ.name] = champ
    return champions


def recieving():
    with open("all_champs.json", 'r') as champfile:
       champsList = json.load(champfile)
       print(champsList)
       return champsList



def print_available_champs(champions: dict[Champion], sock) -> None:

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
    
    #HER!

    #packet = {"Table": available_champs}
    packet = {"data":champions, "command": "Print Champions"}
    packet = json.dumps(packet)
    print(packet)
    #sock.send(packetOfChamps.encode())
    sock.sendall(bytes(packet, encoding="utf-8"))
    #print(available_champs)


def input_champion(prompt: str,
                   color: str,
                   champions: dict[Champion],
                   player1: list[str],
                   player2: list[str]) -> None:

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        match Prompt.ask(f'[{color}]{prompt}'):
            case name if name not in champions:
                print(f'The champion {name} is not available. Try again.')
            case name if name in player1:
                print(f'{name} is already in your team. Try again.')
            case name if name in player2:
                print(f'{name} is in the enemy team. Try again.')
            case _:
                player1.append(name)
                break


def print_match_summary(match: Match) -> None:
    print("her")
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


def read(conn1, conn2, champs):

    data1 = conn1.recv(1024)  
    data2 = conn2.recv(1024)

    sentence1 = data1.decode()
    sentence2 = data2.decode()

    print(sentence1)
    print(sentence2)

    teamOne = sentence1.split()
    teamTwo = sentence2.split()

    return (teamOne, teamTwo)

    '''
    teamOnechamps = []
    teamTwochamps = []

    for name in teamOne:
        for champ in champs:
            if champ["name"] == name:
                teamOnechamps.append(_parse_champ(champ))

    for name in teamTwo:
        for champ in champs:
            if champ["name"] == name:
                teamTwochamps.append(_parse_champ(champ))

    return (teamOnechamps, teamTwochamps)        
    '''
   

#def main(sock) -> None:
def main(sock):
    sock.bind(("localhost", 5555))
    sock.listen()
    #accept(sock)

    while True:

        conn1, adress1 = sock.accept() 
        conn2, adress2 = sock.accept()

        player1Adresse = adress1
        player2Adresse = adress2

        #print('You are player1', conn1, 'from', address1)
        #print('You are player2', conn2, 'from', address2)
        #name: str,
                 #rock: float = 1,
                 #paper: float = 1,
                 #scissors: float 

        #Thread(target=read, args=(conn1, conn2)).start()


        #print_available_champs(champions, sock)
        print('\n')


        #packet = {"data": champions}
        #packet = {"data":champions, "command": "Print Champions"}

        # Henta fra fil med jason, unpacke og sende til client
        

        champsList = recieving()


        packetOfChamps = json.dumps(champsList)
        conn1.send(packetOfChamps.encode())
        #conn1.sendall(bytes(packetOfChamps,encoding="utf-8"))

        conn2.send(packetOfChamps.encode())
        #conn2.sendall(bytes(packetOfChamps,encoding="utf-8"))


        player1, player2 = read(conn1, conn2, packetOfChamps)

        champions = from_json()
        print(champions)

        # Match
        match = Match(
            Team([champions[name] for name in player1]),
            Team([champions[name] for name in player2])
        )
        match.play()

        matchPickle = pickle.dumps(match)

        conn1.send(matchPickle)
        conn2.send(matchPickle)
      








        




if __name__ == '__main__':
    with socket() as sock:
        main(sock)


# Split navn og spillet henter tall verdien til karakterene
# bruke match til å kjøre core til å kjøre spillet
# Se hvordan team local tactics kjører spilelt