import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import numpy as np

class AgePredictor:
    def __init__(self):
        # تصحيح الأوزان والانحيازات
        self.weights = np.array([
            [0.22, 0.22, -0.15, 0.22],
            [8.22, 8.1, 8.2, 0.24],
            [0.28, -0.15, -0.21, 0.27],
            [0.35, -0.13, -0.22, 0.2]
        ])
        self.biases = np.array([-1, 1, 2, 6])
        self.categories = ["18-25", "26-35", "36-50", "51+"]  # تصحيح التسمية من "504" إلى "51+"
    
    def predict(self, data):
        # تصحيح عملية الحساب
        scores = np.dot(self.weights, data) + self.biases
        index = np.argmax(scores)
        return self.categories[index]

class AgeApp(App):
    def build(self):
        self.predictor = AgePredictor()
        self.title = "2026 نظام التنبؤ بالعمر الحيوي"
        
        # التنسيق الرئيسي (رأسي)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        
        # إضافة حقول الإدخال
        layout.add_widget(Label(text="أدخل ضغط الدم:", font_size=18))
        self.bp = TextInput(multiline=False, input_filter="float", hint_text="120")
        layout.add_widget(self.bp)
        
        layout.add_widget(Label(text="أدخل نبض القلب:", font_size=18))
        self.hr = TextInput(multiline=False, input_filter='float', hint_text="70")
        layout.add_widget(self.hr)
        
        layout.add_widget(Label(text="أدخل قوة القبضة:", font_size=18))
        self.grip = TextInput(multiline=False, input_filter='float', hint_text="40")
        layout.add_widget(self.grip)
        
        layout.add_widget(Label(text="أدخل سكر الدم:", font_size=18))
        self.sugar = TextInput(multiline=False, input_filter='float', hint_text="100")
        layout.add_widget(self.sugar)
        
        # زر التوقع
        self.btn = Button(
            text="تحليل البيانات", 
            background_color=(0, 0.7, 0.9, 1), 
            font_size=20
        )
        self.btn.bind(on_press=self.run_prediction)
        layout.add_widget(self.btn)
        
        # ملصق النتيجة
        self.result_label = Label(
            text="النتيجة ستظهر هنا", 
            font_size=24, 
            color=(1, 1, 1, 1)
        )
        layout.add_widget(self.result_label)
        
        return layout
    
    def run_prediction(self, instance):
        try:
            # قراءة البيانات من الواجهة
            data = np.array([
                float(self.bp.text) if self.bp.text else 0,
                float(self.hr.text) if self.hr.text else 0,
                float(self.grip.text) if self.grip.text else 0,
                float(self.sugar.text) if self.sugar.text else 0
            ])
            
            # تنفيذ التنبؤ
            res = self.predictor.predict(data)
            self.result_label.text = f"الفئة العمرية المتوقعة: {res}"
        except ValueError:
            self.result_label.text = "يرجى إدخال أرقام صحيحة"

if __name__ == "__main__":
    AgeApp().run()
