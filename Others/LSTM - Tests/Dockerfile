FROM python:3.6

# Add relevant files
ADD requirements.txt .
ADD Google_Stock_Price_Test.csv .
ADD Google_Stock_Price_Train.csv .
ADD stocks_model.h5 .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY runMe_GetModel.py ./runMe_GetModel.py
COPY runMe_StockResults.py ./runMe_StockResults.py

# Run the application
CMD ["python", "runMe_StockResults.py"]
