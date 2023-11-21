# FastApi

1. 使用ASGI(Asynchronous Server Gateway Interface)框架
2. 使用uvicorn作为ASGI服务器

优点：
1. 速度快
2. 支持异步
3. 代码简洁
4. 类型提示
5. 自动生成文档

安装：
```shell
pip install fastapi
# 安装最小依赖项的 uvicorn
pip install 'uvicorn[standard]'
```

`Pydantic` 是一个用于数据验证的库，它是 FastAPI 的一个依赖项。它提供了一种声明性的方式来定义数据模型，以及在运行时对数据进行验证。

`pip freeze` 查看安装的包

`uvicorn main:app --reload` 启动服务 --reload 热更新


## 路由

> 路由匹配是按照声明的顺序进行的，所以，如果你把 `@app.get("/items/{item_id}")` 放在 `@app.get("/items/me")` 之前，那么 `/items/me` 将永远不会被调用，因为 `/items/{item_id}` 总是会被匹配到。
  
```python
@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get('/items/{item_id}')
async def read_item(item_id: int):
  return {"item_id": item_id}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
  return fake_items_db[skip : skip + limit]

@app.post('/login')
async def login(username: str = Form(), password: str = Form()):
  return {"username": username, "password": password}

class Item(BaseModel):
  name: str
  description: str = None # 可选参数
  price: float
  tax: float = None

@app.post('/create_item')
async def create_item(item: Item):
  return item

@app.post('/files')
async def create_file(file: bytes = File(...)):
  return {"file_size": len(file)}

@app.post('/uploadfile')
async def create_upload_file(file: UploadFile):
  return {"filename": file.filename}

```

formData 参数 需要安装 `python-multipart`
```shell
pip install python-multipart
```

## 中间件

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  process_time = time.time() - start_time
  response.headers["X-Process-Time"] = str(process_time)
  return response
```

推荐以列表的形式添加中间件，这样可以保证中间件的执行顺序
```python
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class CustomHeaderMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request, call_next):
    response = await call_next(request)
    response.headers["X-Custom"] = "Example"
    return response
  
middleware = [
  Middleware(CustomHeaderMiddleware)
]

app = FastAPI(middleware=middleware)
```

fastapi 内置的 middleware
```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
  "http://localhost.tiangolo.com",
  "https://localhost.tiangolo.com",
  "http://localhost",
  "http://localhost:8080",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
```

## jwt
  
```python
from jose import JWTError, jwt


# 加密密钥 openssl rand -hex 32 
SECRET_KEY = '3c2291a895c805b34abdd2c52e2b121c170d13b3c60316cf6468724da9d606e1'

# 设置过期时间 现在时间 + 10小时
expire = datetime.datetime.utcnow() + datetime.timedelta(hours=10)

to_encode = {"exp": expire, "username": "admin", "password": "123321"}

# 加密生成token
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
print(encoded_jwt)

# 解密token
decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=["HS256"])
```