FROM python:3.11-slim  
  
WORKDIR /app  
  
RUN apt-get update && apt-get install -y --no-install-recommends make git && rm -rf /var/lib/apt/lists/*  
  
RUN pip install poetry  
   
COPY pyproject.toml poetry.lock* Makefile README.md* /app/  
  
RUN git init  
  
RUN make setup
  
COPY . /app  
   
CMD ["make", "run-main"]  
