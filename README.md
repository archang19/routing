# routing

**Purpose**: A food delivery logistics program that generates turn-by-turn navigation and delivery instructions

**Methods**:
1. A* Search Algorithm to approximate shortest path between 2 geo-coordinates
2. Traveling Salesman solutions to optimize delivery order
   2a. Brute force solution checking every permutation. O(n!)
   2b. Greedy algorithm that takes shortest delivery each time.
   2c. Two-opt algorithm that repeatedly swaps deliveries until convergence.

**Design**:
A DeliveryPlanner contains:
1. a Mapper to map geocoordinates to street segments
2. a Router to generate optimized point-to-point routing
3. an Optimizer to optimize delivery order

**To Run**:
```
./deliveryPlanner.py
```

**Sample Output**:
```
STARTING FROM: (34.0625329, -118.4470263)
PROCEED NORTH ON Broxton Avenue FOR 0.08 MILES
TURN LEFT ON Le Conte Avenue
PROCEED WEST ON Le Conte Avenue FOR 0.12 MILES
TURN RIGHT ON Levering Avenue
PROCEED NORTHWEST ON Levering Avenue FOR 0.16 MILES
DELIVER Chicken tenders 
PROCEED NORTHEAST ON Strathmore Drive FOR 0.22 MILES
TURN RIGHT ON Strathmore Place
PROCEED EAST ON Strathmore Place FOR 0.23 MILES
DELIVER B-Plate salmon 
PROCEED SOUTH ON Westwood Plaza FOR 0.35 MILES
TURN RIGHT ON Westwood Boulevard
PROCEED SOUTH ON Westwood Boulevard FOR 0.20 MILES
TURN LEFT ON Kinross Avenue
PROCEED EAST ON Kinross Avenue FOR 0.05 MILES
TURN RIGHT ON Glendon Avenue
PROCEED SOUTHEAST ON Glendon Avenue FOR 0.08 MILES
TURN LEFT ON Lindbrook Drive
PROCEED EAST ON Lindbrook Drive FOR 0.09 MILES
TURN LEFT ON Hilgard Avenue
PROCEED NORTHEAST ON Hilgard Avenue FOR 0.16 MILES
DELIVER Pabst Blue Ribbon beer 
TURN RIGHT ON Lindbrook Drive
PROCEED SOUTHWEST ON Lindbrook Drive FOR 0.09 MILES
TURN RIGHT ON Glendon Avenue
PROCEED NORTHWEST ON Glendon Avenue FOR 0.08 MILES
TURN LEFT ON Kinross Avenue
PROCEED WEST ON Kinross Avenue FOR 0.07 MILES
TURN RIGHT ON Broxton Avenue
PROCEED NORTH ON Broxton Avenue FOR 0.15 MILES
TOTAL DISTANCE TRAVELED: 2.16 MILES
```