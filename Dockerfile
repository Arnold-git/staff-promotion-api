FROM python:3.10.10

WORKDIR /staffPromotionAPI

# 
COPY ./app/requirements.txt /staffPromotionAPI/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /staffPromotionAPI/requirements.txt

# 
COPY ./app /staffPromotionAPI/app

# 
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app