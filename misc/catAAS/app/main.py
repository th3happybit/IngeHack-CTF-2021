import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"cat /root/note.txt": "NEVER STOP TALKING ABOUT PALESTINE"}


@app.get("/read_file/{file_path:path}")
def read_file(file_path: str):
    try:
        if not os.path.exists(file_path):
            return {"error": "File not found 😅"}
        if not file_path.startswith('/'):
            return {"error": "Not the right way 🥲"}
        if not os.path.isfile(file_path):
            return {"error": "Not a file 😕"}
        if 'ingehack' in file_path:
            return {"error": "No way 🙂"}
        try:
            return FileResponse(file_path)
        except:
            return {"error": "Failed"}
    except:
        return {"error": "Something went wrong"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, host='0.0.0.0',
                reload=True, access_log=False)
