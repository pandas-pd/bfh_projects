import os
import sys
from scrapy import Api
from datetime import datetime as dt
import numpy as np
import pandas as pd
import time
import neat

#adds systempaths of parent directories to import custom modules
parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
sys.path.insert(1, parent_dir)
import account as ac

parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "..","..")
sys.path.insert(1, parent_dir)
import calls

class Agent():

    def __init__(self, seed_capital):

        self.seed_capital = seed_capital
        self.account_id = ac.Account.create(name="test_agent_blue", balance=seed_capital, currency="ETH")

    def get_balance(self):
        
        self.balance = ac.Get.balance(self.account_id)

    def buy(self, amount):

        ac.Order.buy(account_id=self.account_id, currency="ETH", amount=amount)

    def sell(self, amount):

        ac.Order.sell(account_id=self.account_id, currency="ETH", amount=1)

def get_price():
    new_call= Api()
    new_call.call()
    current_price = new_call.get_currency(currency_pair ="USDT_ETH")

    return current_price

def eval_genomes(genomes, config):

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # agent object that uses that network to work
    nets = []
    agents = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        agents.append(Agent(seed_capital=50))
        ge.append(genome)

    while run and len(agents) > 0:

        time.sleep(0.2)
        now = dt.timestamp(dt.now())
        price = get_price()

        new = np.array([now,price["highestBid"],price["last"]],  dtype=np.float64)

        for x, agent in enumerate(agents):  # give each agent a fitness of 0.1 for each second it stays alive
            ge[x].fitness += 0.1
            agent.get_balance()

            # send agent all info
            output = nets[agents.index(agent)].activate((agent.balance["USDT"], agent.balance["crypto"]*new[2],new[1],new[2]))

            agent.buy(output[0]/new[2]) #we use relu function so we trade exact output amount
            agent.sell(output[1]/new[2]) 
            
            agent.bought= False
            agent.sold= False
            if output[0] > 0:
                agent.bought= True
            if output[1] > 0:
                agent.sold= True

                

        
        # check for bad traders
        for agent in agents:
            if agent.sold == True:
                if agent.balance["crypto"] <=0 :
                    ge[agents.index(agent)].fitness -= 5
                    nets.pop(agents.index(agent))
                    ge.pop(agents.index(agent))
                    agents.pop(agents.index(agent))
            if agent.bought == True:
                if agent.balance["USDT"] <=0 :
                    ge[agents.index(agent)].fitness -= 5
                    nets.pop(agents.index(agent))
                    ge.pop(agents.index(agent))
                    agents.pop(agents.index(agent))

            
            # give more reward for good traders
            if agent.balance["USDT"]> agent.seed_capital:
                for genome in ge:
                    genome.fitness += 5
        
        for agent in agents:
            if agent.balance["USDT"] <= 0 or agent.balance["crypto"] <= 0:
                nets.pop(agents.index(agent))
                ge.pop(agents.index(agent))
                agents.pop(agents.index(agent))



        # break if score gets large enough
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network trading agent.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_ai.txt')
    run(config_path)

    