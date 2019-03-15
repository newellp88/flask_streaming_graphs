FROM python:3
COPY . /graphs
WORKDIR /graphs
RUN pip install -r requirements.txt
CMD ["python", "app.py"]