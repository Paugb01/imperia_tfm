# Sales Forecasting with Machine Learning

## Overview

This project, developed in collaboration with **Imperia** at **Marina de Empresas**, in partnership with **EDEM University**, focuses on creating a solution to **forecast sales** for the company's customers using a machine learning (ML) model. The project leverages **Google Cloud Platform (GCP)** infrastructure and incorporates **XGBoost** as the final model to generate accurate sales predictions. Below is an overview of the project's architecture, deployment, and future improvements.

---

## Table of Contents

- [Sales Forecasting with Machine Learning](#sales-forecasting-with-machine-learning)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Data Handling and Preprocessing](#data-handling-and-preprocessing)
    - [Preprocessing Steps:](#preprocessing-steps)
  - [Machine Learning Models](#machine-learning-models)
    - [Model Selection:](#model-selection)
    - [Evaluation Metrics:](#evaluation-metrics)
  - [Architecture](#architecture)
    - [Technology Stack:](#technology-stack)
  - [Deployment](#deployment)
    - [Kubernetes Architecture:](#kubernetes-architecture)
  - [Improvements and Future Challenges](#improvements-and-future-challenges)
    - [Future Improvements:](#future-improvements)
    - [Challenges:](#challenges)
  - [Conclusion](#conclusion)

---

## Data Handling and Preprocessing

The data used for training the model is sourced from the company's customers. Since each customer provided data in various formats, the first step was to **homogenize** the datasets across the following attributes:
- **Sales records** (sales, date),
- **Point of Sale (POS)**,
- **Customer information**,
- **Product details** (including product features).

### Preprocessing Steps:
1. **Data Cleaning**:
   - Removed inconsistent or incomplete records.
   - Filtered out data from years with insufficient sales volume.
   
2. **Feature Engineering**:
   - Created **lag features** to capture the time-dependent nature of sales data.
   - Used **rolling averages** to smooth short-term fluctuations.
   - Introduced **cyclic features** (e.g., day of the week, month, seasonality indicators).

3. **Data Homogenization**:
   - Standardized the data format across customers to ensure consistency during model training.

---

## Machine Learning Models

After exploring various machine learning models, **XGBoost** was selected as the final model due to its strong performance with structured, tabular data. Other models tested include **Linear Regression**, **ARIMA**, and **Random Forests**.

### Model Selection:
- **XGBoost**: Chosen for its ability to handle complex feature interactions and its suitability for medium-sized datasets.
- **LSTMs (Long Short-Term Memory Networks)**: Initially considered but discarded due to the requirement of large amounts of data.
- **ARIMA**: Tested for time series forecasting but struggled with the multi-dimensional dataset.

### Evaluation Metrics:
- **Root Mean Square Error (RMSE)**: To quantify the deviation of predicted values from actual sales figures.
- **Mean Absolute Percentage Error (MAPE)**: To provide percentage-based accuracy, allowing comparison across different stores or products.

---

## Architecture

The project’s architecture is fully cloud-based, leveraging **Google Cloud Platform (GCP)** and managed workflows via **Cloud Composer (Apache Airflow)**. The architecture consists of the following components:

1. **Cloud Composer (Apache Airflow DAG)**:
   - Orchestrates the end-to-end data pipeline using a DAG with several tasks:
     - **Data Check**: Verifies the presence of raw data in a **Google Cloud Storage (GCS)** bucket.
     - **Data Processing**: Processes the data using **Dataflow** (Apache Beam), performing transformations and loading it into **BigQuery**.
     - **Data Storage**: Stores the cleaned and transformed data in **BigQuery** for analysis and model training.

2. **Model Training**:
   - Data stored in BigQuery is accessed by data scientists to train the machine learning model. The final model (XGBoost) is stored in a **GCS bucket** for future use.

### Technology Stack:
- **Languages**: Python (for scripting and modeling), SQL (for querying data in BigQuery).
- **Services**: GCS, Dataflow, BigQuery, Cloud Composer.

---

## Deployment

Deployment is handled through a **Kubernetes cluster** with three nodes. The architecture includes two key pods:

1. **UI Pod**:
   - Runs a **Streamlit-based UI** that allows users to interact with the system by uploading new data and retrieving sales forecasts.

2. **API Pod**:
   - Hosts the **API** that queries the trained ML model stored in the GCS bucket to perform predictions. This pod is responsible for handling model inference and serving the prediction results to the UI pod.

### Kubernetes Architecture:
- **Nodes**: Three nodes to ensure scalability and availability.
- **Pods**:
   - **Streamlit Pod**: User interface for interacting with the sales forecasting system.
   - **API Pod**: Handles requests from the UI and runs the sales forecast model.

---

## Improvements and Future Challenges

### Future Improvements:
1. **Vertex AI Integration**:
   - We plan to integrate **Vertex AI** to automate model training and deployment. This will be achieved by adding **Vertex AI Airflow operators** to our workflow.
   - By connecting the workflow with **Vertex AI endpoints**, we will streamline the deployment of models, allowing for seamless updates and version control.

2. **Enhanced Training Pipelines**:
   - Automating the model training process using **Vertex AI pipelines** will enable continuous improvement and quicker iteration on models.

### Challenges:
- **Data Availability**:
   - One of the biggest challenges we face is the **lack of sufficient data** from certain customers. This limits the model’s ability to generate accurate predictions. Over time, with better data collection and organization, this can be addressed.
   - Collaborating with customers to improve data consistency and volume will be a key focus moving forward.

---

## Conclusion

This project represents a scalable and cloud-native solution for sales forecasting, leveraging machine learning to provide valuable insights to the company’s customers. Through continuous improvements such as the integration of Vertex AI and enhanced data collection, the system will become even more accurate and robust in the future.

