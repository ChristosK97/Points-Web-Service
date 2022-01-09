# Points-Web-Service
Web service that accepts HTTP requests and returns responses with Python.

## Description
Points-Web-Service is a Python application that has three endpoints to receive calls. JSON data is expected and will return JSON data back. In this system,
there are users that have points in their accounts from transactions. Each transaction record contains the payer (string), points (integer), and timestamp (date).
When points are to be spent, the system doesn't care which payer is spending the points, but the oldest points are to be spent first while no users points go negative.

## Getting Started

### Dependencies
* Python installed on system with pip

### Installation
1. Clone the repo
```
git clone https://github.com/ChristosK97/Points-Web-Service.git
```
2. Install the requirements on a virtual environment through the terminal
```
pip install -r requirements.txt
```
3. Start the server.
```
python webserver.py
```




## Usage
These endpoints were called using Postman in my testing. https://web.postman.co/

There are three endpoints as followed:

**createTransactionAction**: POST endpoint that expects a JSON of a transaction containing the payer, points, and timestamp. This transaction is then added to the system
and returns the list of added transactions.

Example: { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }

![alt text](https://i.imgur.com/SxugkwG.png)

**spendPointsAction**: POST endpoint that expects a JSON of the amount of points to be spent, and returns a JSON with the payers, and how much each spent.

Example: { "points": 5000 }

![alt text](https://i.imgur.com/OQgJBdh.png)

**balances**: GET endpoint that retrieves the balances for each payer.

![alt text](https://i.imgur.com/zTLnXKN.png)

## Bult with

[CherryPy](https://docs.cherrypy.dev/en/latest/) - A pythonic, object-oriented HTTP framework.


