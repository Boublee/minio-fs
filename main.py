import io
import os
from builtins import Exception

from fastapi import FastAPI, status
from fastapi.responses import Response, StreamingResponse
from minio import Minio, error

MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
minio_client = Minio("minio.bobby.org.cn", MINIO_ACCESS_KEY, MINIO_SECRET_KEY)

app = FastAPI()


@app.get("/{bucket_name}/{object_name:path}")
async def get_minio_file(bucket_name: str, object_name: str):
    try:
        content = minio_client.get_object(bucket_name, object_name).read()
    except error.S3Error:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f'get_minio_file 未知错误: {e}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    buffer = io.BytesIO(content)
    return StreamingResponse(buffer, headers={'Content-Type': 'application/download'})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
