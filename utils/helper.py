from fastapi import File, UploadFile


def upload(path: str, file: UploadFile = File(...)):
    try:
        with open(path + file.filename, "wb") as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        raise Exception({"message": "There was an error uploading the file"})
    finally:
        file.file.close()

    return file.filename
