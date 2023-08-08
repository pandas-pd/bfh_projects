import numpy as np
import pandas as pd
import plotly.express as px
import os
import time
import datetime 
import neat
import sys
from agent import Agent

class Data():

    path_data   = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..","data"))
    path_prices = os.path.join(path_data,"prices")
    working_df = None

    def __init__(self,dataset):
        self.df = pd.read_csv(dataset)

class Timer():


    def __init__(self):
        self.start = time.time()
    
    def result(self):
        print("This run took :",time.time() - self.start,"seconds")

def eval_genomes(genomes, config):

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # agent object that uses that network to work
    nets = []
    agents = []
    ge = []

    seed_capital = 100


    for genome_id, genome in genomes:
        genome.fitness = 100
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        agents.append(Agent(seed_capital))
        ge.append(genome)


    df = Data.working_df
    
    reach_factor = 5
    index_count= 40
    

    while len(agents) > 0:

        price_0       = df.iloc[index_count]["last"] 
        price_1       = df.iloc[index_count-(reach_factor*1)]["last"]
        price_2       = df.iloc[index_count-(reach_factor*2)]["last"]
        price_3       = df.iloc[index_count-(reach_factor*3)]["last"]
        price_4       = df.iloc[index_count-(reach_factor*5)]["last"]

        price_f1      = df.iloc[index_count+(reach_factor*1)]["last"]
        price_f2      = df.iloc[index_count+(reach_factor*2)]["last"]
        price_f3      = df.iloc[index_count+(reach_factor*3)]["last"]
        price_f4      = df.iloc[index_count+(reach_factor*4)]["last"]

        for x, agent in enumerate(agents): 
            ge[agents.index(agent)].fitness += 1

            # send agent prices
            output = nets[agents.index(agent)].activate((
                price_0, 
                price_1,
                price_2,
                price_3, 
                price_4, 
                ))

            rate_f1= abs(output[0]  / price_f1)
            rate_f2= abs(output[1]  / price_f2)
            rate_f3= abs(output[2]  / price_f3)
            rate_f4= abs(output[3]  / price_f4)
            
            agent.predict_df = agent.predict_df.append(pd.DataFrame([[
                rate_f1,
                rate_f2,
                rate_f3,
                rate_f4
                ]]))

        # check for bad predictors

        for agent in agents: 
            rate_score= agent.predict_df.iloc[-1].sum(axis=1)
            ge[agents.index(agent)].fitness -= rate_score
            print(rate_score)

        """
        for agent in agents: 
            ge[agents.index(agent)].fitness -= rate_score
            nets.pop(agents.index(agent))
            ge.pop(agents.index(agent))
            agents.pop(agents.index(agent))
        """


        index_count += 1
        

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

    
    ### pre SCRIPT ###
    timer = Timer()
    
    ### SCRIPT ###

    df = Data(os.path.join(Data.path_prices,"price_nov_1.csv"))
    df = df.df
    print("df loaded")
    Data.working_df = df
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_ai.txt')
    run(config_path)

    ### post SCRIPT ###

    timer.result()
    