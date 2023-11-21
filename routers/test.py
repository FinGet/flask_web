from fastapi import APIRouter, File, Form, UploadFile
from pydantic import BaseModel

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


# 路径参数 /items/1
@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# 查询参数 /items/?skip=0&limit=10
@router.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# form 表单参数
@router.post("/login")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}


class Item(BaseModel):
    name: str
    description: str = None  # 可选参数
    price: float
    tax: float = None


# 请求体参数 json
@router.post("/create_item")
async def create_item(item: Item):
    return item


# 路径参数 + 请求体参数
@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


@router.post(
    "/files", tags=["files"], summary="文件上传", description="this is a short desc"
)  # tags 用于分类
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post("/uploadfile", tags=["files"])
async def create_upload_file(file: UploadFile):
    # 可以用markdown语法写文档
    """
    # 上传文件
    ## 文件上传

    - **file**: 上传的文件
    - **filename**: 文件名
    """
    return {"filename": file.filename}
