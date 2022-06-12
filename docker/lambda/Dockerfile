FROM public.ecr.aws/lambda/python:3.9

RUN pip install line-bot-sdk

COPY ./line_notify ./
COPY ./lambda_function.py ./

CMD ["lambda_function.lambda_handler"]
