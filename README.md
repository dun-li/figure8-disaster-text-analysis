# Disaster text message analysis

## Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#file)
4. [Technical Details](#technical)
5. [Conclusions](#conclusions)
6. [Licensing and Acknowledgements](#licensing)

## Installation <a name="installation"></a>
The python file in this project is based on Python 3.6.4. You will need packages such as numpy, pandas, matplotlib, json, plotly, nltk, flask, sklearn, pickle, and re to run the .py file. 

After downloading the repository to your local machine, you  need to follow the steps below:
1. In the terminal, change directory to /data, run the command:
> python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db  

2. Change directory to /models, run the command:  
> python train_classifier.py ../data/DisasterResponse.db classifier.pkl  

3. Change directory to /app, run the command:  
> python run.py

4. You should see some output in the terminal like 'Running on http://0.0.0.0:3001/'. Then, open a browser and open the web link. Now you should be able to see the web page.



## Project Motivation <a name="motivation"></a>
This project builds a multi-label machine learning model to classify disaster text messages. A web application was also developed to classify new disaster text messages.

## File Descriptions <a name="file"></a>
The file structure should be as follows:
> app/  
&emsp;&emsp;template/  
&emsp;&emsp;&emsp;&emsp;master.html  
&emsp;&emsp;&emsp;&emsp;go.html  
&emsp;&emsp;run.py  
data/  
&emsp;&emsp;disaster_categories.csv  
&emsp;&emsp;disaster_messages.csv  
&emsp;&emsp;process_data.py  
&emsp;&emsp;DisasterResponse.db  
models/  
&emsp;&emsp;train_classifier.py  
&emsp;&emsp;classifier.pkl  
README.md  

1. The folder 'app/' is used to run the web application.
2. The folder 'data/' is used for the ETL process. 'disaster_categories.csv' and 'disaster_messages.csv' are raw data files provided by [Figure Eight](https://www.figure-eight.com/). 'process_data.py' is used to clean and transform the raw data. 'DisasterResponse.db' stores the clean data after the ETL process.
3. The folder 'models/' is used for machine learning model training. 'train_classifier.py' is the training script. 'classifier.pkl' stores the trained model.  

## Technical details <a name="technical"></a>

Only two parameters are used for the grid search process. This is to save the training time. If higher accuracy is required, please search more parameter space. You can add more parameters in the build_model() function of the 'train_classifier.py' file.


## Conclusions <a name="conclusions"></a>
Random forest classifier is selected for this project. An average accuracy of 92% can be achieved with a two-minute training. 

## Licensing and Acknowledgements <a name="Licensing"></a>
Thanks [Figure Eight](https://www.figure-eight.com/) for providing the real disaster text messages for the model training. The code in this repository is released under the MIT license. 

