import numpy as np
import pandas as pd
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
    index_count= 0

    performance_df = pd.DataFrame(
        np.array([[seed_capital, 0, 0]]),
        columns=["usdt","btc","revenue"]
    )


    while run and len(agents) > 0:

        #stamp   = df.iloc[index_count]["timestamp"]
        price   = df.iloc[index_count]["last"] 
        ask     = df.iloc[index_count]["lowest_ask"]
        bid     = df.iloc[index_count]["highest_bid"]

        for x, agent in enumerate(agents): 
            ge[agents.index(agent)].fitness += 10


            usdt      = agent.get_usdt() 
            btc       = agent.get_btc()
            revenue   = agent.get_revenue()
            agent.bought    = False
            agent.sold      = False


            # send agent all info
            output = nets[agents.index(agent)].activate((
                price, 
                ask,
                bid,
                usdt, 
                btc, 
                revenue
                ))

            agent.buy(amount  = output[0],price = price) #we use relu function so we trade exact output amount
            agent.sell(amount = output[1],price = price) 
            
            if output[0] > 0:
                agent.bought = True
            if output[1] > 0:
                agent.sold   = True

            if output[0]


        # check for bad traders
        for agent in agents:

            agent.btc       = agent.get_btc()
            agent.usdt      = agent.get_usdt()
            agent.revenue   = agent.get_revenue()

            if agent.sold == True:
                if agent.btc < 0 :
                    ge[agents.index(agent)].fitness -= seed_capital
                    nets.pop(agents.index(agent))
                    ge.pop(agents.index(agent))
                    agents.pop(agents.index(agent))

        for agent in agents: 
            if agent.bought == True:
                if agent.usdt < 0 :
                    ge[agents.index(agent)].fitness -= seed_capital
                    nets.pop(agents.index(agent))
                    ge.pop(agents.index(agent))
                    agents.pop(agents.index(agent))

        for agent in agents:

            if agent.revenue <= ((-1) * seed_capital):
                ge[agents.index(agent)].fitness -= seed_capital
                nets.pop(agents.index(agent))
                ge.pop(agents.index(agent))
                agents.pop(agents.index(agent))
        
        for agent in agents:

            ge[agents.index(agent)].fitness += agent.revenue
            performance_df = performance_df.append(agent.account.iloc[-1])

        index_count += 1
        
        if index_count % 20 == 0:
            performer = performance_df["revenue"]
            horder    = performance_df["btc"]
            saver     = performance_df["usdt"]
            print(df.iloc[index_count])
            print("savers:", saver.max(), saver.min(), saver.mean())
            print("horders:", horder.max(), horder.min(), horder.mean())
            print("performers:", performer.max(), performer.min(), performer.mean())
        

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

    df = Data(os.path.join(Data.path_prices,"usdt_btc.csv"))
    df = df.df
    df = df.drop(range(3700))
    Data.working_df = df
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_ai.txt')
    run(config_path)

    ### post SCRIPT ###

    timer.result()
    