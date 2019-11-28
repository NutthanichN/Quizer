# Quizer
[![Build Status](https://travis-ci.com/NutthanichN/Quizer.svg?branch=master)](https://travis-ci.com/NutthanichN/Quizer)

A single-player quiz game in a form of a racing competition.

## Description
The player chooses a quiz and tries to answer questions correctly to race a racing car across the finish line.
Each quiz contains twenty questions and each question contains four choices. If the player answers a question correctly, 
a racing car will move forward for one unit. The distance between the starting point and the finish line is 
fifteen units, which means the player has to answer at least fifteen questions to reach the finish line.

## Team Members

| Name                   | Roles                    | GitHub                                        |
|------------------------|--------------------------|-----------------------------------------------|
| Nutthanich Narphromar  | Scrum Master, Developer  | [NutthanichN](https://github.com/NutthanichN) |
| Tetach Rattanavikran   | Developer                | [theethaj](https://github.com/theethaj)       |
| Wijantra Cojamnong     | Developer                | [Wijantra](https://github.com/Wijantra)       |


## Documents
- **Project Proposal**: [Project Proposal on Google Docs](https://docs.google.com/document/d/1GN5qD9_AURtWY-XBIucL_acIl1-8UlSZknWD3rw1eYg/edit)
- **Iteration Plans**: [Iteration plans on Google Docs](https://docs.google.com/document/d/1qXjiMyJXYrUlxXa1A0mnS-17RBDQj_wXAGLwbt_dZOQ/edit?usp=sharing)
- **Task Board**: [Task board on Trello](https://trello.com/b/bC1PT5ie/quizer)
- **Iteration Script**: [Iteration Script on Google Docs](https://docs.google.com/document/d/1-wa5WC7MTF3WMeIbpT8Ba_r8_w3ySTaRSiTOx7VoMQI/edit?usp=sharing)
- **Code Review Script**: [Code review script on Google Docs](https://docs.google.com/document/d/1_Wd6kMo92Eimb0DS8xYPQtariomvPAuDKkgVNek5DME/edit?usp=sharing)
- **Code Review Checklist**:[Code review checklist](https://docs.google.com/document/d/1Bs7BH2KkaYmIrOCsnC2gkpXVVRgEXo-XpJFyf1nWCqA/edit?usp=sharing)


## How to run


Step1: Install virtual enviroment
```bash
    pip install virtualenv
```


Step2: Clone this repository and change your current working directory 
```bash
    git clone https://github.com/NutthanichN/Quizer
    cd Quizer
```

Step3: Create new virtual enviroment
```bash
    virtualenv env
```

Step4: Activate virtualenv
```bash
    \path\to\env\Scripts\activate
```

Step5: After activate virtualenv, install all required packages
```bash
    pip install -r requirements.txt
```

Step6: Rename `.env-example` in the root directory of project to `.env`


Step7: Create database tables
```bash
    python manage.py migrate
```

Step8: Load data dump from `quiz_and_player.json`
```bash
    python manage.py loaddata quiz_and_player.json
```

Step9: Run server at localhost:8000
```bash
    python manage.py runserver
```

