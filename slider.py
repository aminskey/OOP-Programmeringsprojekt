from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

class Slider_w_labels:
    def __init__(self, screen, i, minV, maxV, step, text):
        self.text = text
        self.slider = Slider(screen, 110, (i+1)*40, 200, 10, min=minV, max=maxV, step=step)
        self.outputValue = TextBox(screen, 60, 30+i*40, 50, 25, fontsize=15)
        self.outputText = TextBox(screen, 10, 30+i*40, 50, 25, fontSize=15)

        self.outputValue.disable()
        self.outputText.disable()
        self.outputText.setText(self.text)

    def update(self):
        self.outputValue.setText(self.slider.getValue())

    def draw(self):
        self.slider.draw()
        self.outputText.draw()
        self.outputValue.draw()