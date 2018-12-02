# s_invader_game
This is another version of the Space invader I create lately with pygame.
I adapt the game with the PLE (Pygame Learning Environment) which i thank a lot for letting me create an Environnement of Reinforcement Learning

# Installation
1.You may need to install python3 (see for installation : https://www.python.org/)

2.You may need to install pygame (see for installation : https://www.pygame.org/wiki/GettingStarted)

3.You may need to install pillow with : python3 -m pip install Pillow

4.You may need to install the font PressStart2p : https://fonts.google.com/specimen/Press+Start+2P?selection.family=Press+Start+2P


# Starting the game

1.cd ple/games/

2.Starting the game with the dumb neural network : <br> </br>
    -> python3 space_i.py -d <br> </br>
2.Starting the game with the intelligent neural network with the socket <br> </br>
    -> python3 space_i.py -i  <br> </br>
2.For help <br> </br>
    -> python3 space_i.py -h <br> </br>

3.Have fun folks ...


# TODO

- [X] add some plot to compare the Intelligent_neural_network to Dumb_neural_network with a socket (did it but failed need to do it again maybe with only pygame) <br> </br>
- [X] need to resize the window for inserting the graph in the same window of the game <br> </br>
- [ ] fix the issue with the countdown <br> </br>
- [ ] implement some DQN <br> </br>
- [ ] add some gif or video to show the output
