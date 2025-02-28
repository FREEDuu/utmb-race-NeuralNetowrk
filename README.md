# utmb-race-NeauralNetowrk

## In this repo i'll scrape lots of data from the UTMB offical site https://utmb.world/ and try to build a ML model to predict race time

I just need a generic Trail Running Race ( with Distance and Elevation ) and a valid UTMB index ( beetwen 0 - 1000)

## How i scrape the data

Everything i scraped is totally accessible online, for free 
I use the script in api/ folder to do so

## How i train the model

After having access to data, i start by making a Regression Model trained on the dataset i create scraping ( 12 000 + races and 54 000+ runners), I used PyTorch and XGBRegressor / scikit-learn to build , train and evaluate the model 

## Make it accessible via API

I also make a FastAPI app that make this models accessible via api

## RUN the api via FastAPI

make venv and install requirements.txt, in the root folder . . .

```bash

python3 -m venv venv && source ven/bin/activate && pip install -r requirements.txt

```

## start the application with 

```bash

uvicorn api:app --reload

```

and visit the default 

```bash

http://127.0.0.1:8000

```

testing via curl with :

```bash

curl -X POST \
  http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "distance": 120,
    "elevation": 3000,
    "utmb_index": 610
  }'

```
and see the response !! :D