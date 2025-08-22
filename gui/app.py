import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QComboBox, QStackedWidget, QSlider, QHBoxLayout
)
from PyQt5.QtCore import Qt

from core.user import UserProfile
from core.calculator import (
    calculate_bmr,
    calculate_tdee,
    adjust_goal,
    calculate_macros
)
from gui.styles import DARK_STYLE  # put styles in a separate file for cleanliness

class NutritionApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.user = None
        self.setStyleSheet(DARK_STYLE)

        # Init Frames
        self.frame1 = self.init_frame1()
        self.frame2 = self.init_frame2()
        self.frame3 = self.init_frame3()

        self.addWidget(self.frame1)
        self.addWidget(self.frame2)
        self.addWidget(self.frame3)

        self.setCurrentWidget(self.frame1)

    def init_frame1(self):
        """Landing Page (User Profile)"""
        frame = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Set up your profile")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.name = QLineEdit(); self.name.setPlaceholderText("Name")
        self.age = QLineEdit(); self.age.setPlaceholderText("Age")
        self.gender = QComboBox(); self.gender.addItems(["male", "female"])
        self.height = QLineEdit(); self.height.setPlaceholderText("Height (cm)")
        self.weight = QLineEdit(); self.weight.setPlaceholderText("Weight (kg)")

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.go_to_frame2)

        layout.addWidget(title)
        layout.addWidget(self.name)
        layout.addWidget(self.age)
        layout.addWidget(self.gender)
        layout.addWidget(self.height)
        layout.addWidget(self.weight)
        layout.addWidget(next_btn)

        frame.setLayout(layout)
        return frame

    def init_frame2(self):
        """Activities and Goals"""
        frame = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Activities & Goals")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.workouts = QLineEdit(); self.workouts.setPlaceholderText("Workouts per week")
        self.duration = QLineEdit(); self.duration.setPlaceholderText("Duration per workout (min)")
        self.intensity = QComboBox(); self.intensity.addItems(["low", "medium", "high"])
        self.goal = QComboBox(); self.goal.addItems(["gain muscle", "lose fat", "maintain"])

        # Pace Slider
        self.pace_label = QLabel("Pace: standard")
        self.pace_slider = QSlider(Qt.Horizontal)
        self.pace_slider.setMinimum(0)
        self.pace_slider.setMaximum(4)
        self.pace_slider.setValue(2)
        self.pace_slider.setEnabled(False)

        self.pace_map = ["very slow", "slow", "standard", "fast", "very fast"]

        self.goal.currentTextChanged.connect(self.toggle_pace_slider)
        self.pace_slider.valueChanged.connect(self.update_pace_label)

        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.go_to_frame3)

        layout.addWidget(title)
        layout.addWidget(self.workouts)
        layout.addWidget(self.duration)
        layout.addWidget(self.intensity)
        layout.addWidget(self.goal)
        layout.addWidget(self.pace_label)
        layout.addWidget(self.pace_slider)
        layout.addWidget(calc_btn)

        frame.setLayout(layout)
        return frame

    def init_frame3(self):
        """Results Page"""
        frame = QWidget()
        self.results_layout = QVBoxLayout()

        self.summary = QLabel("")
        self.summary.setStyleSheet("font-size: 14px; margin-bottom: 20px;")

        self.calories_label = QLabel("")
        self.calories_label.setStyleSheet("font-size: 32px; font-weight: bold; margin: 20px;")

        self.macro_labels = {}
        macro_row = QHBoxLayout()
        for macro in ["Protein", "Carbs", "Fat"]:
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            self.macro_labels[macro] = lbl
            macro_row.addWidget(lbl)

        retry_btn = QPushButton("Try Again")
        retry_btn.clicked.connect(self.reset_app)

        self.results_layout.addWidget(self.summary, alignment=Qt.AlignCenter)
        self.results_layout.addWidget(self.calories_label, alignment=Qt.AlignCenter)
        self.results_layout.addLayout(macro_row)
        self.results_layout.addWidget(retry_btn, alignment=Qt.AlignCenter)

        frame.setLayout(self.results_layout)
        return frame

    # Navigation + Logic
    def go_to_frame2(self):
        self.user = UserProfile(
            self.name.text(), self.age.text(), self.gender.currentText(),
            self.height.text(), self.weight.text()
        )
        self.setCurrentWidget(self.frame2)

    def go_to_frame3(self):
        self.user.workouts = int(self.workouts.text() or 0)
        self.user.duration = int(self.duration.text() or 0)
        self.user.intensity = self.intensity.currentText()
        self.user.goal = self.goal.currentText()
        self.user.pace = self.pace_map[self.pace_slider.value()]

        bmr = calculate_bmr(self.user)
        tdee = calculate_tdee(bmr, self.user)
        target_cals = adjust_goal(tdee, self.user.goal, self.user.pace)
        protein, carbs, fat = calculate_macros(target_cals, self.user)

        self.summary.setText(f"If you want to {self.user.goal} in a {self.user.pace} pace, you should consume:")
        self.calories_label.setText(f"{int(target_cals)} kcal")
        self.macro_labels["Protein"].setText(f"{protein} g\nProtein")
        self.macro_labels["Carbs"].setText(f"{carbs} g\nCarbs")
        self.macro_labels["Fat"].setText(f"{fat} g\nFat")

        self.setCurrentWidget(self.frame3)

    def toggle_pace_slider(self, goal):
        self.pace_slider.setEnabled(goal == "maintain")

    def update_pace_label(self, value):
        self.pace_label.setText(f"Pace: {self.pace_map[value]}")

    def reset_app(self):
        self.setCurrentWidget(self.frame1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NutritionApp()
    window.show()
    sys.exit(app.exec_())
