from flask import Flask, render_template, request

app = Flask(__name__)


def calculate(num1, num2, operation):
    try:
        num1 = float(num1)
        num2 = float(num2)
    except (ValueError, TypeError):
        return "Ошибка: введите корректные числа"

    try:
        if operation == "add":
            result = num1 + num2
        elif operation == "sub":
            result = num1 - num2
        elif operation == "mul":
            result = num1 * num2
        elif operation == "div":
            if num2 == 0:
                return "Ошибка: деление на ноль"
            result = num1 / num2
        else:
            return "Ошибка: неизвестная операция"
    except Exception as e:
        return f"Ошибка: {e}"

    if result == int(result):
        return str(int(result))
    return f"{result:.4f}".rstrip("0").rstrip(".")


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    num1 = ""
    num2 = ""
    operation = "add"

    if request.method == "POST":
        num1 = request.form.get("num1", "")
        num2 = request.form.get("num2", "")
        operation = request.form.get("operation", "add")
        result = calculate(num1, num2, operation)

    return render_template(
        "index.html",
        result=result,
        num1=num1,
        num2=num2,
        operation=operation,
    )


if __name__ == "__main__":
    app.run(debug=True)