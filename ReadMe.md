# CSC258

Team Members:
John Spaugh
Taro Kumagai
Michael Robertson
Niravkumar Tandel 

Structure:

requires docker-project258Update to run its docker first,
which will call on other dockers to run their applications inside.

Dependencies and evironment:

Web Interface depends on FASTAPI and venv
docker depends on compose.yml for its build
bot interface depend on discord permissions and access to Discord account

Setup:

As mentioned, navigate to the docker-project258Update folder in the command line
run docker compose build
run docker compose up
Open a Discord server in which your account has sufficient permissions to invite bot and invite MuscleBotTest

Execution:

The bot currently supports the following commands:
!test - The bot will respond with "hello [your username]".
!add [number] [number] - The bot will respond with the sum of the two provided numbers
!bluesky ingest [keyword] - The bot will search bluesky for posts featuring the keyword and display information about the first result.
!mastodon ingest - The bot will search Mastodon for posts with the keyword "fitness" and display information about the first result.


CONTRIBUTIONS:
bluesky api - Michael
    all the threads, for example from the top
    also, priority on the most recent posts
    Not all responses?, more focus post that comes out on tree pre-detrmined phrases
    Of the gathered data, then username filter out
    Of the gathered data, then dates filter out
    Of the gathered data, then take out any other unecessary data
    Then obtain data to to be given to another process.
    Setup of dataNode:[posting username, thread title, thread flare/subheader, thread body ]
    
research json -john
    username = string
    date = string
    postcontact = status
    recommandation/processing for the data given
    remove articles of words or search for words, curls push-ups
    Given setup of dataNode:[posting username, thread title, thread flare/subheader, thread body ]
    take date node grom Reddit
    print json of data node
    
docker network - Nirav
    build the architecture for the dockers initially
    setup the pipleline
    MasterController
    -docker coordinator 
    incorperate blueSky software to received data.
    
discord -taro
    discord bot build
    take data and print out on discord through the discord bot
    recieve json
    discord bot convets to plain tex discord message
    discord bot key, need to run shared with group
    
