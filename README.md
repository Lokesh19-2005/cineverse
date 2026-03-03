# CINEVERSE – Movie Recommendation System

## Overview
Deep Learning based Movie Recommendation System using IMDb dataset.

## Project Structure
app.py – Streamlit app  
src/train_model.py – Model training  
src/prepare_dataset.py – Dataset cleaning  
data/movies_cleaned.csv – Processed dataset  
model/recommender_model.h5 – Trained model  

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Run the app:
streamlit run app.py

## Dataset
Download IMDb datasets from:
https://datasets.imdbws.com/

Place the .tsv files locally before running preprocessing.