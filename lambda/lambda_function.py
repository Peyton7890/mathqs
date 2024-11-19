# lambda_function.py
# Author: Peyton Martin
# Description: AWS Lambda function that returns two PDFs of a calculus test and its solutions

import json
import os
import tempfile
import boto3
from TestGenerator import generate_custom_calculus_test, save_problem_pdf, save_solutions_pdf

os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
s3 = boto3.client('s3')

def handler(event, context):
    # ## TEST CODE TODO: Remove this section##
    # # Generate URLs for the uploaded PDFs
    # bucket_name = 'mathqs'  # Replace with your S3 bucket name
    # problems_s3_path = 'problems.pdf'
    # solutions_s3_path = 'solutions.pdf'
    # problems_url = f'https://{bucket_name}.s3.amazonaws.com/{problems_s3_path}'
    # solutions_url = f'https://{bucket_name}.s3.amazonaws.com/{solutions_s3_path}'

    # Parse problem counts from the event
    problem_counts = event.get('problem_counts', {})

    # Generate custom calculus test problems
    test_problems = generate_custom_calculus_test(problem_counts)
    # Create a temporary directory for the PDF files
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Define file paths for the generated PDFs
        problems_pdf_path = os.path.join(tmpdirname, 'problems.pdf')
        solutions_pdf_path = os.path.join(tmpdirname, 'solutions.pdf')

        # Generate the PDFs using Matplotlib
        save_problem_pdf(test_problems, pdf_filename=problems_pdf_path)
        save_solutions_pdf(test_problems, pdf_filename=solutions_pdf_path)

        # Upload PDFs to S3
        bucket_name = 'mathqs'  # Replace with your S3 bucket name
        problems_s3_path = 'problems.pdf'
        solutions_s3_path = 'solutions.pdf'
        
        s3.upload_file(
            problems_pdf_path, 
            bucket_name, 
            problems_s3_path,
            ExtraArgs={'ACL': 'public-read'}
        )
        s3.upload_file(
            solutions_pdf_path, 
            bucket_name, 
            solutions_s3_path,
            ExtraArgs={'ACL': 'public-read'}
        )

        # Generate URLs for the uploaded PDFs
        problems_url = f'https://{bucket_name}.s3.amazonaws.com/{problems_s3_path}'
        solutions_url = f'https://{bucket_name}.s3.amazonaws.com/{solutions_s3_path}'

    # Return the URLs of the generated PDF files
    return {
        'statusCode': 200,
        'body': json.dumps({
            'problems_url': problems_url,
            'solutions_url': solutions_url
        })
    }
