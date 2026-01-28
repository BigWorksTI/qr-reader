from fastapi import FastAPI, UploadFile, File, HTTPException
import cv2
import numpy as np

app = FastAPI()

@app.post("/api/read-qrcode")
async def read_qrcode(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image")

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        return {"content": data or ""}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
