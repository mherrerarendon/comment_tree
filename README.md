# Welcome to Comment Tree!
This is a flask/sqlalchemy sample project that demonstrates how to implement comment threads where each comment in a thread could be the start of a new thread. It also demonstrates the implementation of how to create relevant notifications when new comments are added.

## Virtual environment setup
```
# Run the following commands in the repository directory

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (win)
venv\Scripts\activate.bat

# Activate virtual environment (mac)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Run project in command line
In a terminal with the virtual environment activated, cd to root directory of this repository and enter `python serve.py` 
## Run project unit and integration tests
In a terminal with the virtual environment activated, cd to "ct" dir, and enter `pytest`
## TODO
- Editable app configurations (test vs prod environment)
## References
The project https://github.com/GameSurge/web/tree/master/gsweb was extremely helpful