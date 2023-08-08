from agent import Agent

agent_1 = Agent()
agent_2 = Agent()
agent_3 = Agent()

def printer(agent):
    #print(agent.get_usdt())
    #print(agent.get_btc())
    #print(agent.get_revenue())
    print("\n")

    print(agent.account)

agents = [agent_1,agent_2, agent_3]

for agent in agents:   

    #printer(agent)

    agent.buy(1,1)

    #printer(agent)

    agent.sell(1, 1)

    printer(agent)