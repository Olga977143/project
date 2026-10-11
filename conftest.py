"""Общие фикстуры для тестов."""
import threading
import time

import pytest
from werkzeug.serving import make_server

from app import app as flask_app


@pytest.fixture
def app():
    """Flask-приложение в тестовом режиме."""
    flask_app.config.update({"TESTING": True})
    return flask_app


@pytest.fixture
def client(app):
    """Тестовый клиент Flask (для интеграционных тестов)."""
    return app.test_client()


# --- Живой HTTP-сервер для тестов через requests ---

class _ServerThread(threading.Thread):
    def __init__(self, app, host="127.0.0.1", port=5055):
        super().__init__(daemon=True)
        self.server = make_server(host, port, app)
        self.host, self.port = host, port

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


@pytest.fixture(scope="session")
def live_server():
    """Поднимает Flask на 127.0.0.1:5055 и возвращает базовый URL."""
    flask_app.config.update({"TESTING": True})
    thread = _ServerThread(flask_app)
    thread.start()
    time.sleep(0.3)
    yield f"http://{thread.host}:{thread.port}"
    thread.stop()