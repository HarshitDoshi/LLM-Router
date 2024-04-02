import json
import traceback
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body, Response
from fastapi.responses import StreamingResponse, JSONResponse
from factory import ChatModelFactory

load_dotenv()

app = FastAPI()


@app.post("/chat/", response_class=Response)
async def chat(
    message: str = Body(..., embed=True),
    chat_model_name: str = Body(..., embed=True),
    stream: bool = Body(False, embed=True),
):
    try:
        chat_model = ChatModelFactory.create(chat_model_name)
        if stream:

            async def streamed_responses():
                buffer = ""
                async for response in await chat_model.send_message(
                    message, stream=True
                ):
                    if response is not None:
                        buffer += response
                    else:
                        buffer += ""

                yield (json.dumps({"response": buffer}) + "\n").encode("utf-8")

            return StreamingResponse(
                streamed_responses(), media_type="application/x-ndjson"
            )
        else:
            response = await chat_model.send_message(message, stream=False)
            return JSONResponse(content={"response": response})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An error occurred.")
