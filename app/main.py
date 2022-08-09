import app.utils as utils
from fastapi import FastAPI, Response


app = FastAPI()



@app.get("/avatar/{uuid_str}",
        responses = {
             200: {
                 "content": {"image/png": {}}
             }
            },
        response_class=Response,)
async def get_avatar_from_uuid(uuid_str: str):
    head = utils.get_skin_from_uuid(uuid_str)
    return Response(head, media_type="image/png")
