# capstone-dv-final
Serverless Image Processing Pipeline 

This project implements a serverless image processing workflow using AWS services. It resizes uploaded images and stores the output in a separate S3 bucket, triggered via API Gateway and orchestrated with Step Functions.

Architecture Overview
FLOW
* API Gateway receives the POST request (/process)

* Step Functions orchestrates the workflow (imageworkflow-vd)

* Lambda Function (ProcessImage) resizes the image using Pillow

* S3 Bucket (image-reiszed-vd) stores the output image

* CloudWatch monitors logs and execution metrics

  ```

+---------------------+     +----------------------+     +------------------------+     +------------------------+
|    API Gateway      | --> |   Step Functions     | --> |   Lambda Function      | --> |   S3: resizes-image-dv |
+---------------------+     +----------------------+     +------------------------+     +------------------------+
        ^                                                                                                      
        |                                                                                                      
+---------------------+                                                                                       
|     CloudWatch      |                                                                                       
+---------------------+
```

Prerequisites
Before deploying, ensure the following:

AWS Resources
An active AWS account with access to:

* S3

* Lambda

* Step Functions

* API Gateway

* IAM

Lambda Layer
* A custom Pillow layer built for the same Python runtime as your Lambda function (e.g., Python 3.12)

* Uploaded to AWS Lambda Layers and attached to the function


Deployment Instructions

1. S3 Buckets
    * Create an input bucket named original-images-vd

    * Create an output bucket named image-reiszed-vd

        * Inside the output bucket, create a folder named thumbnails/

2. Lambda Function
    * Create a function named ProcessImage using Python 3.12

    * Attach the Pillow layer

    * Set the following environment variables:

        * OUTPUT_BUCKET = resized-image-cap

        * OUTPUT_PREFIX = thumbnails/

        * SUPPORTED_SUFFIXES = .jpg,.jpeg,.png


    * Ensure the Lambda execution role has permissions to read from the input bucket and write to the output bucket


3. Step Functions Workflow

    * Create a state machine named imageworkflow-cap

    * Include states to invoke the Lambda function, check the result, and log success or failure

    * Set the Lambda timeout to at least 30 seconds to avoid timeouts during image processing

4. API Gateway
    * Create a REST API with a resource path /process

    * Configure a POST method that triggers the Step Functions workflow

    * Ensure the API Gateway integration role has permission to start executions of the state machine


Final API Endpoint
Once deployed, trigger the workflow using a POST request to:

https://658lmta4h4.execute-api.ca-central-1.amazonaws.com/prod/process

Include a JSON body with:

    * bucket: original-images-vd

    * key: name of the uploaded image (e.g.sample.jpg, new-sample.jpg)
