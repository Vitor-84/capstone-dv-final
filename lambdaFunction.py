import boto3
from PIL import Image
import os
import io

s3 = boto3.client('s3')
output_bucket = os.environ['OUTPUT_BUCKET']
THUMB_W = int(os.environ.get('THUMB_W', '300'))
THUMB_H = int(os.environ.get('THUMB_H', '300'))

def lambda_handler(event, context):
    try:
        source_bucket = event['bucket']
        source_key = event['key']

        obj = s3.get_object(Bucket=source_bucket, Key=source_key)
        img_data = obj['Body'].read()

        image = Image.open(io.BytesIO(img_data))
        image.thumbnail((THUMB_W, THUMB_H))

        buffer = io.BytesIO()
        fmt = (image.format or 'JPEG')
        image.save(buffer, format=fmt)
        buffer.seek(0)

        base = source_key.rsplit('/', 1)[-1]
        name, ext = os.path.splitext(base)
        output_key = f"thumbnails/{name}_thumb{ext or '.jpg'}"

        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=buffer.getvalue(),
            ContentType=f"image/{fmt.lower()}"
        )

        return {"status": "success", "file": output_key}
    except Exception as e:
        return {"status": "error", "message": str(e)}

