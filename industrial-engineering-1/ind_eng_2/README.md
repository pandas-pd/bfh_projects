# Mini projects

## Mini project 1
 - Due at 2022-11-01


## Requirements

Build a working scale that meets accuracy class III
- The scale can be turned on and off.
- The scale has a tara function.
- The scale has a calibrate sequence.
- When starting up the scale, a zero calibration have to be performed.

## JSON
- from frontend {on: True, tara: False, calibrate: False}
- from backend:
     - format: {weight: int, on: True}
     - if calibrate, weight will be:
         - -1e5 = cal0
         - -2e5 = cal1
         - -3e5 = cal2

## Research 

Klasse 3 bis 500g:
- 0 ≤ m ≤ 500 e Eichfehlergrenze +- 0.5 e, Werkfehlergrenze +- 1 e (0.1 * 0.5 = 0.05 g)
- e = 0.1 (e ist ein Wert, den ich als Waagenbauer selber bestimme anhand dem maximum Gewicht bestimme)
