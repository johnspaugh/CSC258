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

Ensure Discord API key is properly placed in \\ContainerMuscleBot\\MuscleBot\\config\\config.json, it must be placed manually because Discord deactivates API keys which are shared online as a security measure.
As mentioned, navigate to the docker-project258Update folder in the command line
run docker compose build
run docker compose up
Open a Discord server in which your account has sufficient permissions to invite bot and invite MuscleBotTest

# CSC 258 Distributed Systems Project - Kubernetes Setup Guide

## Overview

This project uses:

- Docker
- Docker Compose
- Kubernetes (Docker Desktop Kubernetes)
- Python microservices
- C#/.NET microservices
- Horizontal Pod Autoscaling (HPA)
- Discord Bot integration

Main services:

- `musclebot`
- `dataingestionbluesky`
- `dataingestionmastodon`
- `dataprocessing`
- `userprofileservice`
- `logdatabase`

---

# 1. Start Docker Desktop

Open Docker Desktop and ensure:

- Docker is running
- Kubernetes is enabled

Verify Kubernetes:

```bash
kubectl get nodes
```

Expected output:

```text
desktop-control-plane   Ready
```

---

# 2. Navigate to Project Root

All build/import commands below are run from the **project root**.

---

# 3. Build Docker Images

## MuscleBot

```bash
docker build -t musclebot:latest -f ./ContainerMuscleBot/MuscleBot/Dockerfile ./ContainerMuscleBot/MuscleBot
```

## Bluesky Ingestion

```bash
docker build -t dataingestionbluesky:latest -f ./dataingestionbluesky/Dockerfile ./dataingestionbluesky
```

## Mastodon Ingestion

```bash
docker build -t dataingestionmastodon:latest -f ./dataIngestionMastodon/Dockerfile ./dataIngestionMastodon
```

## Data Processing

```bash
docker build -t dataprocessing:latest -f ./dataprocessing/Dockerfile ./dataprocessing
```

## User Profile Service

```bash
docker build -t userprofileservice:latest -f ./ContainerUserProfile/UserProfileService/Dockerfile ./ContainerUserProfile/UserProfileService
```

## Log Database

```bash
docker build -t logdatabase:latest -f ./ContainerLogDatabase/Dockerfile ./ContainerLogDatabase
```

---

# 4. Import Docker Images Into Kubernetes

These commands are also run from the **project root**.

## MuscleBot

```bash
docker save musclebot:latest -o musclebot.tar
docker cp musclebot.tar desktop-control-plane:/musclebot.tar
docker exec desktop-control-plane sh -c "ctr -n k8s.io images import /musclebot.tar"
```

## Bluesky Ingestion

```bash
docker save dataingestionbluesky:latest -o dataingestionbluesky.tar
docker cp dataingestionbluesky.tar desktop-control-plane:/dataingestionbluesky.tar
docker exec desktop-control-plane sh -c "ctr -n k8s.io images import /dataingestionbluesky.tar"
```

## Mastodon Ingestion

```bash
docker save dataingestionmastodon:latest -o dataingestionmastodon.tar
docker cp dataingestionmastodon.tar desktop-control-plane:/dataingestionmastodon.tar
docker exec desktop-control-plane sh -c "ctr -n k8s.io images import /dataingestionmastodon.tar"
```

## Data Processing

```bash
docker save dataprocessing:latest -o dataprocessing.tar
docker cp dataprocessing.tar desktop-control-plane:/dataprocessing.tar
docker exec desktop-control-plane sh -c "ctr -n k8s.io images import /dataprocessing.tar"
```

## User Profile Service

```bash
docker save userprofileservice:latest -o userprofileservice.tar
docker cp userprofileservice.tar desktop-control-plane:/userprofileservice.tar
docker exec desktop-control-plane sh -c "ctr -n k8s.io images import /userprofileservice.tar"
```

## Log Database

```bash
docker save logdatabase:latest -o logdatabase.tar
docker cp logdatabase.tar desktop-control-plane:/logdatabase.tar
docker exec desktop-control-plane sh -c "ctr -n k8s.io images import /logdatabase.tar"
```

---

# 5. Apply Kubernetes YAML Files

Navigate to the Kubernetes folder:

```bash
cd k8s
```

Apply all Kubernetes resources:

```bash
kubectl apply -f .
```

---

# 6. Verify Kubernetes Resources

## Check Pods

```bash
kubectl get pods
```

Expected services:

```text
musclebot
dataingestionbluesky
dataingestionmastodon
dataprocessing
userprofileservice
logdatabase
```

All pods should eventually show:

```text
Running
```

## Check Services

```bash
kubectl get services
```

## Check Horizontal Pod Autoscaling

```bash
kubectl get hpa
```

---

# 7. View Logs

## MuscleBot Logs

```bash
kubectl logs -l app=musclebot -f
```

## Bluesky Ingestion Logs

```bash
kubectl logs -l app=dataingestionbluesky -f
```

## Mastodon Ingestion Logs

```bash
kubectl logs -l app=dataingestionmastodon -f
```

## Data Processing Logs

```bash
kubectl logs -l app=dataprocessing -f
```

## User Profile Service Logs

```bash
kubectl logs -l app=userprofileservice -f
```

## Log Database Logs

```bash
kubectl logs -l app=logdatabase -f
```

---

# 8. Test The System

Use Discord commands through the Discord bot.

Current system flow:

```text
Discord User
    ↓
musclebot
    ↓
dataingestionbluesky OR dataingestionmastodon
    ↓
dataprocessing
    ↓
musclebot
    ↓
Discord response
    ↓
logdatabase
```

---

# 9. Watch Autoscaling

## Watch HPA Changes

```bash
kubectl get hpa -w
```

## Watch Pod Scaling

```bash
kubectl get pods -w
```

---

# 10. Updating Code After Changes

If code changes, rebuild and re-import only the affected service.

Example for `dataprocessing`:

Run from project root:

```bash
docker build -t dataprocessing:latest -f ./dataprocessing/Dockerfile ./dataprocessing

docker save dataprocessing:latest -o dataprocessing.tar

docker cp dataprocessing.tar desktop-control-plane:/dataprocessing.tar

docker exec desktop-control-plane sh -c "ctr -n k8s.io images import /dataprocessing.tar"
```

Restart deployment:

```bash
kubectl rollout restart deployment dataprocessing
```

---

# 11. Stop Everything

Run from the `k8s` directory:

```bash
kubectl delete -f .
```

---

# Notes

- `musclebot` intentionally does NOT autoscale.
- Main scalable services are:
  - `dataingestionbluesky`
  - `dataingestionmastodon`
  - `dataprocessing`
- Kubernetes service names must exactly match the hostnames used in code.
- If pods show `ErrImageNeverPull`, the image was not imported into Kubernetes correctly.
- If a service shows `Connection refused`, check:
  - pod status
  - service names
  - service selectors
  - pod logs


Execution:

The bot currently supports the following commands:
!test - The bot will respond with "hello \[your username]".
!add \[number] \[number] - The bot will respond with the sum of the two provided numbers
!bluesky ingest \[keyword] - The bot will search bluesky for posts featuring the keyword and display information about the first result.
!mastodon ingest - The bot will search Mastodon for posts with the keyword "fitness" and display information about the first result.

To see the results on the alternative web-browser API endpoint 
use the following: http://127.0.0.1:8000

Close Setup:

As mentioned before, navigate back to the same terminal holding the running docker containers at the docker-project258Update folder in the command line. Then input the following to shut done the running docker containters.
Crtl+C
docker compose down


CONTRIBUTIONS:
bluesky api - Michael
all the threads, for example from the top
also, priority on the most recent posts
Not all responses?, more focus post that comes out on tree pre-detrmined phrases
Of the gathered data, then username filter out
Of the gathered data, then dates filter out
Of the gathered data, then take out any other unecessary data
Then obtain data to to be given to another process.
Setup of dataNode:\[posting username, thread title, thread flare/subheader, thread body ]

research json -john
username = string
date = string
postcontact = status
recommandation/processing for the data given
remove articles of words or search for words, curls push-ups
Given setup of dataNode:\[posting username, thread title, thread flare/subheader, thread body ]
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

