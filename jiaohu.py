import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("信号显示GUI")
        self.resize(600, 500)

        # ===== 1. 创建控件 =====
        self.btn1 = QPushButton("绘制连续信号 cos(t)")
        self.btn2 = QPushButton("绘制离散信号 cos(n)")
        self.text = QTextEdit()
        self.text.setPlaceholderText("这里显示信息...")

        # 图形区域
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # ===== 2. 布局 =====
        layout = QVBoxLayout()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.text)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # ===== 3. 绑定事件 =====
        self.btn1.clicked.connect(self.plot_continuous)
        self.btn2.clicked.connect(self.plot_discrete)

    # ===== 4. 连续信号 =====
    def plot_continuous(self):
        t = np.linspace(0, 2*np.pi, 1000)
        y = np.cos(t)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(t, y)
        ax.set_title("连续信号 cos(t)")
        ax.grid()

        self.canvas.draw()

        self.text.append("已绘制连续信号 cos(t)")

    # ===== 5. 离散信号 =====
    def plot_discrete(self):
        n = np.arange(0, 20)
        x = np.cos(n)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.stem(n, x)
        ax.set_title("离散信号 cos(n)")
        ax.grid()

        self.canvas.draw()

        self.text.append("已绘制离散信号 cos(n)")


# ===== 主程序 =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())