from scripts import *
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QSpinBox, QLabel, QLineEdit, QHBoxLayout
from PySide6.QtCore import Slot, QThread, Signal


class RunScriptThread(QThread):
    error_occurred = Signal(str)
    script_finished = Signal()

    def __init__(self, fgo_script, rounds, task, team):
        super().__init__()
        self.fgo_script = fgo_script
        self.rounds = rounds
        self.task = task
        self.team = team
        self.stop_flag = False

    def run(self):
        try:
            self.fgo_script.week(self.rounds, self.task, self.team)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.script_finished.emit()


def handle_error(error_message):
    # Here you can handle the error, for example, show a message box to the user.
    print(f"An error occurred: {error_message}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.run_thread = None
        self.fgo_script = None
        self.match_counter = 0

        # === Window Title ===
        self.setWindowTitle("FGO Script")

        # === Window Size ===
        self.layout = QVBoxLayout()

        # === Task Selection ===
        self.task_label = QLabel("Select Task:")
        self.layout.addWidget(self.task_label)
        self.task_select = QComboBox()
        self.task_select.addItem("QP", 0)
        self.task_select.addItem("EXP", 1)
        self.layout.addWidget(self.task_select)
        
        # === Team Selection ===
        self.team_label = QLabel("Select Team:")
        self.layout.addWidget(self.team_label)
        self.team_select = QComboBox()
        self.team_select.addItem("Blue Team", 0)
        self.team_select.addItem("Red Team", 1)
        self.layout.addWidget(self.team_select)

        # === Rounds Selection ===
        self.rounds_label = QLabel("Select Rounds:")
        self.layout.addWidget(self.rounds_label)
        self.rounds_select = QSpinBox()
        self.rounds_select.setMinimum(1)
        self.layout.addWidget(self.rounds_select)

        # === Counter ===
        self.counter_label = QLabel("Current matches: 0")
        self.layout.addWidget(self.counter_label)

        # === Buttons ===
        self.run_button = QPushButton("Run FGO Script")
        self.run_button.clicked.connect(self.run_fgo_script)
        self.layout.addWidget(self.run_button)

        self.stop_button = QPushButton("Stop FGO Script")
        self.stop_button.clicked.connect(self.stop_fgo_script)
        self.layout.addWidget(self.stop_button)

        self.screenshot_button = QPushButton("Take Screenshot")
        self.screenshot_button.clicked.connect(self.take_screenshot)
        self.layout.addWidget(self.screenshot_button)

        # === Tap ===
        self.tap_label = QLabel("Tap:")
        self.layout.addWidget(self.tap_label)
        self.xy_layout = QHBoxLayout()
        self.x_label = QLabel("X:")
        self.xy_layout.addWidget(self.x_label)
        self.x_input = QLineEdit()
        self.xy_layout.addWidget(self.x_input)
        self.y_label = QLabel("Y:")
        self.xy_layout.addWidget(self.y_label)
        self.y_input = QLineEdit()
        self.xy_layout.addWidget(self.y_input)
        self.layout.addLayout(self.xy_layout)

        self.tap_button = QPushButton("Tap")
        self.tap_button.clicked.connect(self.tap_action)
        self.layout.addWidget(self.tap_button)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    @Slot()
    def take_screenshot(self):
        self.fgo_script.dc.take_screenshot()

    @Slot()
    def tap_action(self):
        x = int(self.x_input.text())
        y = int(self.y_input.text())
        self.fgo_script.dc.tap(x, y)

    def count_and_add(self, template_path, threshold=0.97):
        """Count the number of times a template appears in a screenshot and add it to the match_counter."""
        self.fgo_script.dc.take_screenshot()
        main_image = cv2.imread('image/screenshot.png')
        main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_path, 0)

        res = cv2.matchTemplate(main_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # zip the locations and get the unique coordinates (thus getting rid of overlapping locations)
        locations = list(set(list(zip(*loc[::-1]))))

        # Add the number of matches to the counter
        self.match_counter += len(locations)
        print(f"Current matches: {self.match_counter}")
        self.counter_label.setText(f"Current matches: {self.match_counter}")

    @Slot()
    def run_fgo_script(self):
        task = self.task_select.currentData()
        team = self.team_select.currentData()
        rounds = self.rounds_select.value()

        self.run_thread = RunScriptThread(self.fgo_script, rounds, task, team)
        self.run_thread.error_occurred.connect(handle_error)
        self.run_thread.script_finished.connect(self.update_match_counter)
        self.run_thread.start()

    @Slot()
    def stop_fgo_script(self):
        if self.run_thread is not None:
            self.run_thread.stop_flag = True

    def set_fgo_script(self, fgo_script):
        self.fgo_script = fgo_script

    @Slot()
    def update_match_counter(self):
        self.counter_label.setText(f"Current matches: {self.match_counter}")
