import os
import sys
import tempfile
from typing import Optional

from path_handler import PathManager
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import (
    SummerizerConfig,
    PipelineConfig,
    Prompt,
    Client,
    AudioFormat,
    Language,
    Provider,
    PipelineType,
)
from src.pipeline.factory import SummarizingPipelineFactory
from src.clients.factory import ClientFactory
from src.prompts.factory import PromptFactory

app = FastAPI()
origins = ["https://localhost:8000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# app.mount("/src/ui", StaticFiles(directory="src/ui"), name="ui") # ! Debugger
app.mount("/ui", StaticFiles(directory="ui"), name="ui")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serves the main HTML page for the web interface.

    Returns:
        FileResponse: The HTML file for the web interface.
    """
    # return FileResponse("src/ui/base.html") # ! Debugger
    return FileResponse("ui/base.html")

def detect_pipeline_type(file_extension: Optional[str]) -> PipelineType:
    """
    Detects the pipeline type based on the file's extension.

    Args:
        file_extension (Optional[str]): The file extension (e.g., "mp4", "wav", "txt").

    Returns:
        PipelineType: The type of pipeline (e.g., VIDEO, AUDIO, TEXT).
    """
    if file_extension:
        file_extension = file_extension.lower()
        if file_extension in {"mp4", "mkv", "avi", "mov"}:
            return PipelineType.VIDEO
        elif file_extension in {"wav", "mp3", "ogg", "flac"}:
            return PipelineType.AUDIO
        elif file_extension in {"txt", "md"}:
            return PipelineType.TEXT
    
    return PipelineType.TEXT


@app.post("/summarize")
async def summarize(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: str = Form(...),
    audio_format: str = Form(...),
    prompt: str = Form(...),
    client: str = Form(...),
    model: str = Form(...),
):
    """
    Handles the summarization request.

    Args:
        file (Optional[UploadFile]): The uploaded file (video, audio, or text).
        text (Optional[str]): The input text (if no file is uploaded).
        language (str): The language of the input.
        audio_format (str): The audio format for conversion.
        prompt (str): The summarization prompt type.
        client (str): The LLM client to use.
        model (str): The model to use for summarization.

    Returns:
        dict: A dictionary containing the summarized text.

    Raises:
        HTTPException: If no file or text is provided, or if an error occurs during processing.
    """
    try:
        if not file and not text:
            raise HTTPException(status_code=400, detail="No file or text provided")

        input_data = None
        pipeline_type = None
        temp_file_path = None

        if file:
            file_extension = file.filename.split(".")[-1] if file.filename else "tmp"
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                temp_file_path = temp_file.name
                file_content = await file.read()
                temp_file.write(file_content)

            pipeline_type = detect_pipeline_type(file_extension)
            input_data = temp_file_path
        else:
            input_data = text
            pipeline_type = PipelineType.TEXT

        language = Language(language)
        audio_format = AudioFormat(audio_format)
        prompt = PromptFactory.create(Prompt(prompt))
        client = ClientFactory.create(Client(client))

        summerizer_config = SummerizerConfig(
            prompt=prompt,
            client=client,
            model=model,
        )

        pipeline_config = PipelineConfig(
            summerizer_config=summerizer_config,
            audio_format=audio_format,
            provider=Provider.VOSK,
            language=language,
            pipeline_type=pipeline_type,
        )

        pipeline = SummarizingPipelineFactory.create(pipeline_config)
        summary = pipeline.summarize(input_data)
        
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return {"summary": summary}

    except Exception as e:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)