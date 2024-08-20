from flask import Flask, request, render_template

app = Flask(__name__)

class ModelTrainerR1:
    def __init__(self, config_path):
        self.config_path = config_path
        self.arguments = {}

    @staticmethod
    def load_config(config_path):
        # 模拟加载配置文件
        return {
            'total_round': 10,
            'start_round': 0,
            'data_size': 100,
            'mode': 'default'
        }

    def set_arguments(self, total_round, start_round, data_size, mode):
        self.arguments['total_round'] = total_round
        self.arguments['start_round'] = start_round
        self.arguments['data_size'] = data_size
        self.arguments['mode'] = mode
        print(f"Arguments set: {self.arguments}")

    def execute(self):
        print("Executing with arguments:", self.arguments)
        print("Model is running...")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo1/", methods=["POST"])
def run_pipeline_research1():
    print("Handling request!")

    # 检查是否是实例化模型的请求
    if 'config_path' in request.form:
        config_path = request.form.get('config_path', 'chemprop_run/config/config.yaml')
        print(f"Instantiating ModelTrainerR1 with config path: {config_path}")
        
        # 加载配置文件并实例化模型
        config = ModelTrainerR1.load_config(config_path)
        arg_list = []
        config_list = ['total_round', 'start_round', 'data_size', 'mode']
        
        for i in config_list:
            value = request.form.get(i)
            arg_list.append(value if value != '' else config.get(i))
        
        # 实例化ModelTrainerR1
        global chemporpR1
        chemporpR1 = ModelTrainerR1(config_path)
        chemporpR1.set_arguments(
            total_round=arg_list[0], 
            start_round=arg_list[1], 
            data_size=arg_list[2], 
            mode=arg_list[3]
        )
        print("ModelTrainerR1 instantiated.")

    # 检查是否是执行模型的请求
    if 'execute_model' in request.form:
        print("Executing ModelTrainerR1...")
        if 'chemporpR1' in globals():
            chemporpR1.execute()
        else:
            print("Error: ModelTrainerR1 must be instantiated before execution.")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
