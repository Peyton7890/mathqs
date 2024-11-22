FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt and install Python packages
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY CalcProblemGenerator.py ${LAMBDA_TASK_ROOT}
COPY TestGenerator.py ${LAMBDA_TASK_ROOT}

# Set handler
CMD [ "lambda_function.handler" ]