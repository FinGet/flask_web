# flask_web

pip install flask

> 要注意安装在哪个版本下的，不同的版本之间不能from import


### 渲染html

两种方式：

1. 直接返回
```python
def index():
    return '<h1>Hello World!</h1>'
```

2. 通过模板渲染

```python
def index():
    return render_template('index.html')
```

### url_for
> ，该参数是后端定义的函数名称，这里是upload_file。它会自动解析并生成该函数所对应的路由URL。
```html
<form action="{{ url_for('upload_file') }}"></form>
// 等价于
<form action="/upload"></form>
```
