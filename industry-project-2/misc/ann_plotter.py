import pandas as pd
import numpy as np 
import plotly.express as px

class Networkplotter():

    def plot_ann(arch = [10,3,2,1], title = "ANN architecture"):

        structure = Networkplotter.create_neurons(arch) #df
        connections = Networkplotter.create_connections(structure, arch) #dict
        Networkplotter.draw_network(structure, connections, arch, title)

    def create_neurons(arch):

        structure = {
            "layer_pos"  : [],
            "neuron_pos" : [],
        }

        max_neurons = max(arch)
        mid_pos = max_neurons / 2

        for i in range(len(arch)):

            neuron_pos = mid_pos - (arch[i] / 2)

            for neuron in range(arch[i]):

                structure["layer_pos"].append(i),
                structure["neuron_pos"].append(neuron_pos)
                neuron_pos += 1

        return pd.DataFrame(structure)

    def create_connections(structure, arch):

        connections = {
            "x" :   [], #(x1,x2), (x1,x2), layer_pos
            "y" :   [], #(y1,y2), (y1,y2), neuron_pos
        }

        relevant_layers = list(range(len(arch)))[:-1]
        relevant_neurons = structure.loc[structure["layer_pos"].isin(relevant_layers)]

        for i in range(relevant_neurons.shape[0]):

            x1 = structure.iloc[i]["layer_pos"]
            y1 = structure.iloc[i]["neuron_pos"]
            x2 = x1 + 1

            for j in structure.loc[structure["layer_pos"] == x2].index.tolist():
                y2 = float(structure.iloc[j]["neuron_pos"])

                connections["x"].append((x1,x2))
                connections["y"].append((y1,y2))

        return connections

    def draw_network(structure, connections, arch, title):

        width   = len(arch) * 150
        height  = 700
        structure["size"] = 1

        fig_base = px.scatter(
            data_frame = structure,
            x = "layer_pos",
            y = "neuron_pos",
            size_max = 10,
            size = "size",

            title = title,

            width = width,
            height = height,
            #color = "neuron_pos",
            labels = {"layer_pos" : "layer", "neuron_pos" : "",}
        )

        data = fig_base.data
        for i in range(len(list(connections["x"]))):

            fig_base.add_shape(
                type='line',
                x0 = connections["x"][i][0], y0 = connections["y"][i][0],
                x1 = connections["x"][i][1], y1 = connections["y"][i][1],
                line=dict(color="lightgrey", width=2),
                layer = "below",
            )

        tick_text = list(range(len(arch)))
        tick_text[0] = "Input layer"
        tick_text[-1] = "Output layer"

        fig_base.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = list(range(len(arch))),
                ticktext = tick_text,
            )
        )

        #unlcean code
        fig_base.update_yaxes(showticklabels=False)
        fig_base.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        fig_base.update_layout({
            "plot_bgcolor": "rgba(255, 255, 255, 255)",
            "paper_bgcolor": "rgba(255, 255, 255, 255)",
            })

        fig_base.show()
