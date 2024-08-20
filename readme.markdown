# Flask 示例项目：使用两个表单触发不同操作

## 1. 项目简介

这是一个基于 Flask 的 Web 应用示例，演示了如何通过两个不同的表单触发不同的操作：
- **第一个表单**用于实例化 `ModelTrainerR1` 类，并传递一些可选的配置参数。
- **第二个表单**用于执行已实例化的 `ModelTrainerR1` 对象的 `execute` 方法。

## 2. 注意要点

# 为什么 `chemporpR1` 要实例化为全局变量

在你的代码中，`chemporpR1` 被实例化为全局变量，是为了确保在不同的请求中都可以访问到这个对象。下面是为什么需要将它设为全局变量的原因：

## 1. Flask 的请求处理机制

Flask 是一个基于 WSGI 的 Web 框架，它在每次请求时都会创建一个新的上下文（request context）。这意味着每次处理 HTTP 请求时，函数（如 `run_pipeline_research1`）都会在新的上下文中执行，函数内部的局部变量在请求结束后就会被销毁。

## 2. 持续存储对象实例

在你的示例中，有两个不同的操作：
- **实例化 `ModelTrainerR1`**：这是通过一个表单请求完成的，目的是加载配置文件并创建一个 `ModelTrainerR1` 对象。
- **执行 `ModelTrainerR1` 的方法**：这是通过另一个表单请求完成的，目的是调用已经实例化的 `ModelTrainerR1` 对象的 `execute` 方法。

为了在这两个不同的请求中都能访问同一个 `ModelTrainerR1` 实例，你需要将实例保存到一个在整个应用程序上下文中都可访问的地方。这就是为什么 `chemporpR1` 被定义为全局变量的原因。

## 3. 全局变量的作用

通过将 `chemporpR1` 设为全局变量，你确保了：
- 第一个请求中实例化的 `ModelTrainerR1` 对象在后续的请求中仍然可用。
- 当你在后续请求中调用 `chemporpR1.execute()` 时，它能够访问到之前设置的参数和状态。

## 注意事项

虽然全局变量能解决这个问题，但它也有潜在的缺点，比如：
- **线程安全问题**：在多线程环境下，多个请求可能会同时访问或修改这个全局变量，导致意外行为。
- **复杂性增加**：全局变量可能导致代码的可维护性降低，因为它们可能在多个地方被修改，导致难以追踪程序的状态。

## 替代方案

一个常见的替代方案是使用 Flask 的应用上下文或会话来保存这些对象，或者考虑使用数据库或缓存系统（如 Redis）来持久化和管理状态。

```python
from flask import g

@app.before_request
def before_request():
    g.chemporpR1 = None

@app.route("/demo1/", methods=["POST"])
def run_pipeline_research1():
    print("Handling request!")

    if 'config_path' in request.form:
        config_path = request.form.get('config_path', 'chemprop_run/config/config.yaml')
        config = ModelTrainerR1.load_config(config_path)
        arg_list = []
        config_list = ['total_round', 'start_round', 'data_size', 'mode']
        
        for i in config_list:
            value = request.form.get(i)
            arg_list.append(value if value != '' else config.get(i))
        
        g.chemporpR1 = ModelTrainerR1(config_path)
        g.chemporpR1.set_arguments(
            total_round=arg_list[0], 
            start_round=arg_list[1], 
            data_size=arg_list[2], 
            mode=arg_list[3]
        )

    if 'execute_model' in request.form:
        if g.chemporpR1:
            g.chemporpR1.execute()
        else:
            print("Error: ModelTrainerR1 must be instantiated before execution.")

    return render_template('index.html')

```


# 4 Flask `g` 对象和独立表单请求的解释

## Flask `g` 对象

`flask.g` 是 Flask 提供的一个全局对象，用于在请求的生命周期中存储和共享数据。它是一个请求上下文对象，为每个请求提供独立的命名空间。

### 如何工作

- `g` 对象在每个请求开始时创建，并在请求结束时清除。
- 每个请求都拥有自己的 `g` 对象实例，确保数据隔离。
- 在请求处理的不同阶段（如视图函数、钩子函数等），可以通过 `g` 对象访问和存储数据。

### 作用

1. **在请求上下文中共享数据**：可以在视图函数和其他处理阶段之间共享数据。
2. **避免使用全局变量**：提供了独立的请求上下文，避免了多线程和并发访问中的全局变量问题。
3. **简化代码**：可以减少函数之间的数据传递，提高代码的可读性。

### 示例

```python
from flask import Flask, g, request

app = Flask(__name__)

@app.before_request
def before_request():
    g.user = request.args.get('user')  # 在请求前获取并存储用户信息

@app.route('/')
def index():
    return f"Hello, {g.user}!"  # 在视图函数中访问存储的用户信息

if __name__ == '__main__':
    app.run(debug=True)
```