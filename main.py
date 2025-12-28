from fastapi import FastAPI, UploadFile, File, Response
from scripts.burpsuite.ai_ingest import ingest_burp_xml

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()
    # xmltodict expects string, so decode bytes to string
    xml_content = content.decode('utf-8')
    markdown_output = ingest_burp_xml(xml_content)
    return Response(content=markdown_output, media_type="text/markdown")
