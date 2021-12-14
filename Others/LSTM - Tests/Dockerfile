FROM python:3.6


# Install dependencies
# RUN pip install -r requirements.txt
RUN pip install --upgrade pip

RUN pip install numpy
RUN pip install matplotlib
RUN pip install pandas
RUN pip install sklearn
RUN pip install keras
RUN pip install tensorflow

ADD Google_Stock_Price_Test.csv .
ADD Google_Stock_Price_Train.csv .
ADD stocks_model.h5 .

COPY runMe_GetModel.py ./runMe_GetModel.py
COPY runMe_StockResults.py ./runMe_StockResults.py

# Run the application
CMD ["python", "runMe_StockResults.py"]
