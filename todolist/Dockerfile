FROM python:3.10

ENV HOME /todolist
WORKDIR $HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#ENTRYPOINT ["python3"]
CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]