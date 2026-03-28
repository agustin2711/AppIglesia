import json
import time
import boto3
from botocore.exceptions import ClientError

#Conectar base de datos
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table('AppIglesia')

#CORS HEADERS
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,PATCH,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

def response(status, body):
    return {
        "statusCode": status,
        "headers": CORS_HEADERS,
        "body": json.dumps(body) if body != "" else ""
    }

def lambda_handler(event, context):
    try:
        method = event["requestContext"]["http"]["method"]
        path_params = event.get("pathParameters") or {}
        id = path_params.get("id")

        #Version del texto
        query = event.get("queryStringParameters") or {}
        version_param = query.get("version")
        client_version = int(version_param) if version_param is not None else None

        if method == "OPTIONS":
            return response(200, "")

        if not id:
            return response(400, {"ok": False, "error": "Falta id"})

        
        if method == "GET":
            return leer(id,client_version)

        if method == "PATCH":
            body = json.loads(event.get("body") or "{}")
            texto = body.get("texto")

            if not texto:
                return response(400, {"ok": False, "error": "Falta texto"})

            return actualizar(id, texto)

        return response(405, {"ok": False, "error": "Método no permitido"})

    except Exception as e:
        return response(500, {"ok": False, "error": str(e)})

#------------------------------------------
#--- READ (LEER)
#------------------------------------------
def leer(id, client_version):
    if client_version is None:
        r = table.get_item(Key={"id": id})
        item = r.get("Item")

        if not item:
            return response(404, {"ok": False, "error": "No existe"})

        return response(200, {
            "ok": True,
            "texto": item.get("texto", ""),
            "version": int(item.get("version", 0))
        })

    timeout = 25
    start = time.time()

    while True:
        r = table.get_item(Key={"id": id})
        item = r.get("Item")

        if not item:
            return response(404, {"ok": False, "error": "No existe"})

        db_version = int(item.get("version", 0))

        if db_version != client_version:
            return response(200, {
                "ok": True,
                "texto": item.get("texto", ""),
                "version": db_version
            })

        if time.time() - start > timeout:
            return response(204, "")

        time.sleep(1)



#------------------------------------------
#--- UPDATE (ACTUALIZAR)
#------------------------------------------
def actualizar(id, texto):
    try:
        r = table.update_item(
            Key={"id": id},
            UpdateExpression="SET texto = :texto ADD version :inc",
            ExpressionAttributeValues={
                ":texto": texto,
                ":inc": 1
            },
            ReturnValues="ALL_NEW"
        )

        return response(200, {
            "ok": True,
            "texto": r["Attributes"]["texto"],
            "version": int(r["Attributes"]["version"])
        })
    except ClientError as e:
        return response(500, {
            "ok": False,
            "error": e.response["Error"]["Message"]
        })

    