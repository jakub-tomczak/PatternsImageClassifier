FROM python

ENV PROJECT_ROOT=/patterns_recognition
# clone code (this may also be done by copying )
RUN git clone https://github.com/jakub-tomczak/PatternsImageClassifier.git ${PROJECT_ROOT}

WORKDIR $PROJECT_ROOT
# install required packages
RUN pip install -r $PROJECT_ROOT/requirements.txt
# run main.py
# we may use ENTRYPOINT as well, however it doesn't pass signals
CMD ["python", "main.py"]