 
FROM python:3.10.14

 
RUN apt-get update && apt-get install -y git

ARG VER
ARG OPENAI_API_KEY
 
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6 \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7 \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

 
RUN fc-cache -f -v

 
RUN git clone https://github.com/wixxxez/wrapmade_poc .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN git checkout ${VER}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

 
EXPOSE 8501

 
CMD git pull && streamlit run streamlit_app.py