"""
lambda_function.py
Author: Peyton Martin
Description: AWS Lambda handler for the MathQs test generator.
Flow:
    1. Receives problem counts from API Gateway
    2. Generates test problems and solutions
    3. Creates PDFs using matplotlib
    4. Uploads PDFs to S3
    5. Returns signed URLs for PDF access
"""

import json
import os
import tempfile
import boto3
import traceback

from TestGenerator import generate_custom_calculus_test, save_problem_pdf, save_solutions_pdf

s3 = boto3.client('s3')

def handler(event, context):
    """
    AWS Lambda handler function for test generation.
    
    Args:
        event (dict): API Gateway event or direct Lambda invocation payload
        context: AWS Lambda context
    
    Returns:
        dict: API Gateway response with PDF URLs
    """
    try:
        # Handle both direct Lambda invocation and API Gateway event
        if isinstance(event, dict):
            if 'body' in event:
                # API Gateway event
                body = json.loads(event['body'])
                problem_counts = body.get('problem_counts', body)
            else:
                # Direct Lambda invocation
                problem_counts = event
        else:
            problem_counts = {}

        if not problem_counts:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No problem counts provided'})
            }

        # Set up environment
        os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
        
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
        
    except Exception as e:
        error_msg = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'traceback': error_msg
            })
        }
