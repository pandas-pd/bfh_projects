Why not usin GNNs?
 - The data is not really graph data
	- What are nodes and node features?
	- What are edged and edge features?
 - If still should be used, how should this be formated?
 - GNNs are mostly used for:
	- Node classification (How can a new node be labeled as?)
	- Link prediction (How does the link look like?)

How to prepear the data?
 - join the forecast data to the scada data?
	- on what base?
	- which forecast period is relevant ? (72h)
	- multiple scada points with one forecast?

What is to be predicted with the ML-Model?
 - The poweroutput according to scada and forecast data? (ML)
 - The poweroutput according to pc and forecast data? (Simple Calculation)

How should the process look like? (Regressor)
 - Create forecast models
 - Compare forecast of scada with pc?
 - See if lower or higher?
 - If so, find the reasons why this is (which feature influecnes these)?
 
