# AI-Powered AML Platform

## Overview
This is a **full-stack web application** for detecting suspicious financial transactions and reducing money laundering risks. The platform uses **AI/ML models** to analyze transaction patterns, counterparty behavior, and customer profiles in real-time.

## Features
- **Transaction Scoring:** ML model computes risk scores for each transaction.
- **Alerts Dashboard:** Shows top suspicious transactions with reasons.
- **Interactive Frontend:** React + TailwindCSS dashboard.
- **Backend API:** FastAPI endpoints for scoring and alerts.
- **Database Integration:** PostgreSQL stores transaction history and alerts.

## Tech Stack
- Frontend: React, TailwindCSS, Axios
- Backend: FastAPI, Python, Pydantic
- Machine Learning: scikit-learn (Gradient Boosting)
- Database: PostgreSQL
- Deployment: Docker-ready

## Getting Started

### Backend
```bash
cd backend
python -m venv venv
# Activate venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app/models/train_model.py  # Generates aml_model.pkl
uvicorn app. main: app --reload

