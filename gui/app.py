import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QSlider,
)
from PyQt5.QtCore import Qt

from core.user import UserProfile
from core.calculator import calculate_bmr, calculate_tdee, adjust_goal, calculate_macros
from gui.styles import DARK_STYLE, LIGHT_STYLE


class NutritionApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.user = None
        self.mode = None
        self.pace_map = ["very slow", "slow", "standard", "fast", "very fast"]

        # Track selected buttons
        self.gender_choice = None
        self.intensity_choice = None
        self.goal_choice = None

        # Frames
        self.frame0 = self.init_frame0()  # Landing
        self.frame1 = self.init_frame1()  # User Profile
        self.frame2 = self.init_frame2()  # Activities & Goals
        self.frame3 = self.init_frame3()  # Results

        self.addWidget(self.frame0)
        self.addWidget(self.frame1)
        self.addWidget(self.frame2)
        self.addWidget(self.frame3)

        self.setCurrentWidget(self.frame0)

    # ---------------- Utility ----------------
    def reset_button_styles(self, buttons, selected_btn):
        """Resets all buttons, highlights the selected one."""
        for btn in buttons:
            btn.setStyleSheet("")
        selected_btn.setStyleSheet("background-color: #555; font-weight: bold;")

    # ---------------- Frame 0 ----------------
    def init_frame0(self):
        layout = QVBoxLayout()
        title = QLabel("Nutrition Tracker App")
        title.setStyleSheet("font-size: 42px; font-weight: bold;")
        subtitle = QLabel("elmer2-fl")
        subtitle.setStyleSheet("font-size: 18px;")

        dark_btn = QPushButton("Dark Mode")
        dark_btn.clicked.connect(lambda: self.set_mode("dark"))

        light_btn = QPushButton("Light Mode")
        light_btn.clicked.connect(lambda: self.set_mode("light"))

        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)
        layout.addWidget(dark_btn, alignment=Qt.AlignCenter)
        layout.addWidget(light_btn, alignment=Qt.AlignCenter)

        frame = QWidget()
        frame.setLayout(layout)
        return frame

    def set_mode(self, mode):
        self.mode = mode
        if mode == "dark":
            self.setStyleSheet(DARK_STYLE)
        else:
            self.setStyleSheet(LIGHT_STYLE)
        self.setCurrentWidget(self.frame1)

    # ---------------- Frame 1 ----------------
    def init_frame1(self):
        frame = QWidget()
        layout = QVBoxLayout()

        title = QLabel("User Profile")
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        # Input fields
        self.name_field = self.create_labeled_input("Name")
        self.age_field = self.create_labeled_input("Age")
        self.height_field = self.create_labeled_input("Height (cm)")
        self.weight_field = self.create_labeled_input("Weight (kg)")

        # Gender buttons
        gender_label = QLabel("Gender")
        gender_layout = QHBoxLayout()
        self.male_btn = QPushButton("Male")
        self.female_btn = QPushButton("Female")
        gender_layout.addWidget(self.male_btn)
        gender_layout.addWidget(self.female_btn)

        def select_gender(choice, btn):
            self.gender_choice = choice
            self.reset_button_styles([self.male_btn, self.female_btn], btn)

        self.male_btn.clicked.connect(lambda: select_gender("male", self.male_btn))
        self.female_btn.clicked.connect(
            lambda: select_gender("female", self.female_btn)
        )

        # Navigation
        nav_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.setCurrentWidget(self.frame0))

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.go_to_frame2)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(next_btn)

        # Assemble layout
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addLayout(self.name_field)
        layout.addLayout(self.age_field)
        layout.addWidget(gender_label)
        layout.addLayout(gender_layout)
        layout.addLayout(self.height_field)
        layout.addLayout(self.weight_field)
        layout.addLayout(nav_layout)

        frame.setLayout(layout)
        return frame

    def create_labeled_input(self, label_text):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        field = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(field)
        return layout

    # ---------------- Frame 2 ----------------
    def init_frame2(self):
        frame = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Activities & Goals")
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        # Workouts per week
        self.workouts_field = self.create_labeled_input(
            "How often do you workout in a week?"
        )

        # Duration
        self.duration_field = self.create_labeled_input(
            "How long does a workout last? (minutes)"
        )

        # Intensity buttons
        intensity_label = QLabel("How intense are the workouts?")
        self.easy_btn = QPushButton("Easy")
        self.medium_btn = QPushButton("Medium")
        self.hard_btn = QPushButton("Hard")

        def set_intensity(choice, btn):
            self.intensity_choice = choice
            self.reset_button_styles(
                [self.easy_btn, self.medium_btn, self.hard_btn], btn
            )

        self.easy_btn.clicked.connect(lambda: set_intensity("easy", self.easy_btn))
        self.medium_btn.clicked.connect(
            lambda: set_intensity("medium", self.medium_btn)
        )
        self.hard_btn.clicked.connect(lambda: set_intensity("hard", self.hard_btn))

        intensity_layout = QHBoxLayout()
        intensity_layout.addWidget(self.easy_btn)
        intensity_layout.addWidget(self.medium_btn)
        intensity_layout.addWidget(self.hard_btn)

        # Goal buttons
        goal_label = QLabel("What is your goal?")
        self.gain_btn = QPushButton("Gain muscle")
        self.lose_btn = QPushButton("Lose fat")
        self.maintain_btn = QPushButton("Maintain")

        def set_goal(choice, btn):
            self.goal_choice = choice
            self.reset_button_styles(
                [self.gain_btn, self.lose_btn, self.maintain_btn], btn
            )
            self.pace_slider.setVisible(choice in ["gain muscle", "lose fat"])
            self.pace_label.setVisible(choice in ["gain muscle", "lose fat"])

        self.gain_btn.clicked.connect(lambda: set_goal("gain muscle", self.gain_btn))
        self.lose_btn.clicked.connect(lambda: set_goal("lose fat", self.lose_btn))
        self.maintain_btn.clicked.connect(
            lambda: set_goal("maintain", self.maintain_btn)
        )

        goal_layout = QHBoxLayout()
        goal_layout.addWidget(self.gain_btn)
        goal_layout.addWidget(self.lose_btn)
        goal_layout.addWidget(self.maintain_btn)

        # Pace slider
        self.pace_label = QLabel("Pace: standard")
        self.pace_label.setVisible(False)
        self.pace_slider = QSlider(Qt.Horizontal)
        self.pace_slider.setMinimum(0)
        self.pace_slider.setMaximum(4)
        self.pace_slider.setValue(2)
        self.pace_slider.setVisible(False)
        self.pace_slider.valueChanged.connect(
            lambda v: self.pace_label.setText(f"Pace: {self.pace_map[v]}")
        )

        # Navigation
        nav_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.setCurrentWidget(self.frame1))
        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.go_to_frame3)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(calc_btn)

        # Assemble
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addLayout(self.workouts_field)
        layout.addLayout(self.duration_field)
        layout.addWidget(intensity_label)
        layout.addLayout(intensity_layout)
        layout.addWidget(goal_label)
        layout.addLayout(goal_layout)
        layout.addWidget(self.pace_label)
        layout.addWidget(self.pace_slider)
        layout.addLayout(nav_layout)

        frame.setLayout(layout)
        return frame

    # ---------------- Frame 3 ----------------
    def init_frame3(self):
        frame = QWidget()
        layout = QVBoxLayout()

        self.result_label = QLabel("Results will appear here")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("font-size: 24px;")

        self.calories_label = QLabel("")
        self.calories_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        self.macros_label = QLabel("")
        self.macros_label.setStyleSheet("font-size: 22px;")

        try_again_btn = QPushButton("Try Again")
        try_again_btn.clicked.connect(lambda: self.setCurrentWidget(self.frame0))

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.setCurrentWidget(self.frame2))

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(try_again_btn)

        layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.calories_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.macros_label, alignment=Qt.AlignCenter)
        layout.addLayout(nav_layout)

        frame.setLayout(layout)
        return frame

    # ---------------- Navigation ----------------
    def go_to_frame2(self):
        # Save user profile
        self.user = UserProfile(
            self.name_field.itemAt(1).widget().text(),
            self.age_field.itemAt(1).widget().text(),
            self.gender_choice,
            self.height_field.itemAt(1).widget().text(),
            self.weight_field.itemAt(1).widget().text(),
        )
        self.setCurrentWidget(self.frame2)

    def go_to_frame3(self):
        # Perform calculations
        bmr = calculate_bmr(self.user)
        tdee = calculate_tdee(bmr, self.intensity_choice)
        adjusted = adjust_goal(
            tdee,
            self.goal_choice,
            (
                self.pace_map[self.pace_slider.value()]
                if self.pace_slider.isVisible()
                else "standard"
            ),
        )
        protein, carbs, fat = calculate_macros(adjusted)

        # Update results
        self.result_label.setText(
            f"If you want to {self.goal_choice} in a {self.pace_map[self.pace_slider.value()] if self.pace_slider.isVisible() else 'standard'} pace, you should consume:"
        )
        self.calories_label.setText(f"{adjusted:.0f} Calories")
        self.macros_label.setText(
            f"Protein: {protein:.0f}g   Carbs: {carbs:.0f}g   Fat: {fat:.0f}g"
        )

        self.setCurrentWidget(self.frame3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NutritionApp()
    window.show()
    sys.exit(app.exec_())
