# s_invader_game
This is another version of the Space invader I create lately with pygame.
I adapt the game with the PLE (Pygame Learning Environment) which i thank a lot for creating an Environnement of Reinforcement Learning

# Installation
1.You need to install python3 (see for installation : https://www.python.org/)

2.You need to install pygame (see for installation : https://www.pygame.org/wiki/GettingStarted)

3.install pillow with : python3 -m pip install Pillow

4.install matplotlib with : python -m pip install -U matplotlib

# Starting the game

1.cd PyGame-Learning-Environment/ple/games/

2.Starting the game with the dumb neural network :
   _ python3 space_i.py -d
2.Starting the game with the intelligent neural network with the socket
  _ python3 space_i.py -i -n 127.0.0.1 -p 13370

2.To see the graph of the dumb neural network (naive qlearning agent)
  _ python3 space_i.py -gd

2.To see the graph of the intelligent network (qlearning)
  _ python3 space_i.py -gi

2.For help
  _ python3 space_i.py -h

3.Have fun folks ...


# TODO

1.[ ] add some plot to compare the Intelligent_neural_network to Dumb_neural_network with a socket (did it but failed need to do it again)
2.[ ] implement some DQN
