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

@app.get("/tailored_avatar/{uuid_str}",
        responses = {
             200: {
                 "content": {"image/png": {}}
             }
            },
        response_class=Response,)
async def get_tailored_avatar_from_uuid(uuid_str: str):
    uuid = utils.string_to_uuid(uuid_str)
    skin_value = utils.get_tailor_skin_value_from_uuid(uuid)
    return Response(utils.get_head_from_value(skin_value), media_type="image/png")