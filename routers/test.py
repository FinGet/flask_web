from enum import Enum
from typing import List, Optional
from fastapi import (
    APIRouter,
    Body,
    File,
    Form,
    HTTPException,
    Header,
    Path,
    Query,
    Response,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field

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


## pydantic 模型声明请求体参数
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


# UploadFile 与 bytes 相比有更多优势；更适于处理图像、视频、二进制文件等大型文件，好处是不会占用所有内存
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


## 可选文件上传
@router.post("/uploadfile/optional", tags=["files"])
async def create_upload_file(file: Optional[UploadFile] = File(None)):
    return {"filename": file.filename}


## 多文件上传
@router.post("/uploadfiles", tags=["files"])
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


## 枚举类型声明路径参数
class Animal(str, Enum):
    cat = "cat"
    dog = "dog"
    fish = "fish"


@router.get("/test/animal/{animal}", tags=["test"], summary="枚举类型定义路径参数")
async def test_animal(animal: Animal):
    if animal == Animal.cat:
        return {"animal": animal, "message": "meow"}
    if animal == Animal.dog:
        return {"animal": animal, "message": "woof"}
    return {"animal": animal}


## 包含路径的路径参数 /test/file/xxx/xxx
## path 表明这个参数应该匹配任意路径
@router.get("/test/file/{file_path:path}", tags=["test"], summary="文件路径参数")
async def test_file(file_path: str):
    return {"file_path": file_path}


## 长度和正则表达式验证
@router.get("/test/len/{number}/{regex}", tags=["test"], summary="长度和正则表达式验证")
async def test_len(
    number: int = Path(..., gt=10, le=20), regex: str = Path(..., regex="^a")
):
    # gt 大于 le 小于 eq 等于 ge 大于等于 lt 小于等于 ne 不等于
    return {"number": number, "regex": regex}


## 校验query参数
@router.get("/test/query", tags=["test"], summary="校验query参数")
async def test_query(q: str = Query(..., min_length=3, max_length=50, regex="^a")):
    return {"q": q}


## 同时声明请求体、路径、查询参数
# 如果在路径中也声明了该参数，它将被用作路径参数。 item_id
# 如果参数属于单一类型（比如 int、float、str、bool 等）它将被解释为查询参数。q, short
# 如果参数的类型被声明为一个 Pydantic 模型，它将被解释为请求体。item
@router.post("/test/body/{item_id}", tags=["test"], summary="同时声明请求体、路径、查询参数")
async def test_body(item_id: int, item: Item, q: str = None, short: bool = False):
    item_dict = item.dict()
    if q:
        item_dict.update({"item_id": item_id, "q": q})
    if not short:
        item_dict.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item_dict


class Image(BaseModel):
    url: str
    name: str


## 多个请求体参数
@router.post("/test/multiple_body", tags=["test"], summary="多个请求体参数")
async def test_multiple_body(item: Item, img: Image):
    return [item, img]


## 请求体中单一类型的数据
@router.post("/test/single_body", tags=["test"], summary="请求体中单一类型的数据")
async def test_single_body(id: int = Body()):
    return {"id": id}


## 请求体中单一类型的数据
@router.post("/test/single_body2", tags=["test"], summary="请求体中单一类型的数据")
async def test_single_body(id: int = Body(..., embed=True)):
    return {"id": id}


## 请求体中嵌入单一参数
@router.post("/test/single_body3", tags=["test"], summary="请求体中嵌入单一参数")
async def test_single_body(item: Item = Body(embed=True)):
    return {"item": item}


## 列表请求体
@router.post("/test/list_body", tags=["test"], summary="列表请求体")
async def test_list_body(items: list[Item]):
    return {"items": items}


## 请求体参数示例
# field同Path、Query、Body可以设置default、title等信息
class City(BaseModel):
    country: str = "中国"
    provence: str = Field(..., example="四川")  # Field可以定义请求体的格式和类型
    citys: Optional[List] = None
    population: int = Field(default=None, title="人口数", ge=1000)

    class Config:
        schema_extra = {  # schema_extra用于定义请求体的示例
            "example": {
                "country": "中国",
                "provence": "四川",
                "citys": ["绵阳", "成都", "遂宁", "..."],
                "population": 66666666,
            }
        }


@router.post("/test/city", tags=["test"], summary="请求体参数示例")
async def test_city(city: City):
    return city


## 设置cookie
@router.get("/test/cookie", tags=["test"], summary="设置cookie")
async def test_cookie(cookie: str, response: Response):
    response.set_cookie(key="test", value=cookie)
    return {"message": "Come to the dark side, we have cookies"}


## 读取header信息
@router.get("/test/header", tags=["test"], summary="读取header信息")
async def test_header(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


## 响应模型
@router.get("/test/response", tags=["test"], summary="响应模型", response_model=Item)
async def test_response():
    return Item(name="Foo", description="There comes my hero", price=4.2, tax=0.1)


## repose_model_exclude_unset 响应模型中排除未设置的属性
@router.get(
    "/test/response_exclude_unset",
    tags=["test"],
    summary="响应模型",
    response_model=Item,
    response_model_exclude_unset=True,
)
async def test_response_exclude_unset():
    return Item(name="Foo", description="There comes my hero", price=4.2, tax=0.1)


## response_model_include 响应模型中包含指定的属性
@router.get(
    "/test/response_include",
    tags=["test"],
    summary="响应模型",
    response_model=Item,
    response_model_include={"name", "price"},
)
async def test_response_include():
    return Item(name="Foo", description="There comes my hero", price=4.2, tax=0.1)


## response_model_exclude 响应模型中排除指定的属性
@router.get(
    "/test/response_exclude",
    tags=["test"],
    summary="响应模型",
    response_model=Item,
    response_model_exclude={"tax"},
)
async def test_response_exclude():
    return Item(name="Foo", description="There comes my hero", price=4.2, tax=0.1)


## 状态码
@router.get(
    "/test/status", tags=["test"], summary="状态码", status_code=status.HTTP_200_OK
)
async def test_status():
    return {"message": "Status code is 200"}


## 错误处理
@router.get("/test/error", tags=["test"], summary="错误处理")
async def test_error():
    raise HTTPException(status_code=404, detail="Item not found")


## 自定义错误处理
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@router.get("/test/unicorn/{name}", tags=["test"], summary="自定义错误处理")
async def test_unicorn(name: str):
    if name == "yue":
        return {"unicorn_name": name}
    else:
        raise UnicornException(name=name)
