## FastAPI Demo

  ```sh
  # 安装包 (进入到 backend 文件夹)
  pip install -r ./requirements.txt
  
  # 找到 main.py 中的 主函数, 右键启动
  ```

  ```sh
	-- api									    # 接口文件夹
    -- common                   # 公共文件夹
    -- core                     # 核心文件夹
        -- config.py              # 配置文件夹
    -- crud                     # 数据库增删改查文件夹
    -- models                   
        -- database               # mysql 表模型
        -- redis                  # redis 表模型
    -- register                 # 注册中心
    -- schemas                  # 模型文件夹 (Java中的实体类或者VO视图类)
    -- static                   # 静态文件夹
    -- utils                    # 工具文件夹
    -- Dockerfile               # 后端服务部署文件
    -- main.py                  # 项目启动文件
    -- requirements.txt         # 所需的包
  ```

### 1. Python 版本：Python 3.11

+ 使用了 Python 新语法, 最低版本要求 3.10

```python
# 变动语法

Union[int, float] -> int | float
Optional[int] -> int | None
```

### 2. 关于 Session

+ 在 `Github `上找到这个 [request.session in HTTP Middleware · Issue #4746 · tiangolo/fastapi (github.com)](https://github.com/tiangolo/fastapi/issues/4746)

+ 尝试使用 `starlette` 提供的 `SessionMiddleware`，在<font color="red">项目启动后（前端清除 cookie 之后）</font>第一次请求拿不到 `sessionId`，实例代码如下：

  ```python
  # 安装包 https://fastapi.tiangolo.com/#optional-dependencies
  python install -U itsdangerous
  ```

  ```python
  from fastapi import FastAPI
  from pydantic import BaseModel
  from starlette.middleware.cors import CORSMiddleware
  from starlette.middleware.sessions import SessionMiddleware
  from starlette.requests import Request
  
  app = FastAPI()
  
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_origin_regex="http://localhost:3000",
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  
  app.add_middleware(
      SessionMiddleware,
      session_cookie="sessionId", # session key name
      secret_key="some-random-string", # 密钥, 加密 session value
      same_site="none",
      https_only=True,
      max_age=24 * 60 * 60
  )
  
  
  class UserLogin(BaseModel):
      name: str
      password: str
  
  
  @app.post("/api/user/login")
  def user_login(user: UserLogin, request: Request):
      request.session["test"] = "123" # 必须设置session属性
      print(request.session)
      print(request.cookies)
      return {"code": 0, "msg": "Success", "data": ""}
  
  
  @app.get("/api/user/")
  def user_login():
      return {"code": 0, "msg": "Success", "data": {"test": "123"}}
  ```

+  [FastAPI Sessions (jordanisaacs.github.io)](https://jordanisaacs.github.io/fastapi-sessions/)，暂未尝试...

### 3. 关于 `Redis` 序列化 

+ 详见 [RedisJson](https://zxiaosi.com/archives/26a72a9d.html)