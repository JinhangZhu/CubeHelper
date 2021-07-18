# -*- coding: utf-8 -*-
# @Time     : 2021/7/18 21:15
# @Author   : Jinhang
# @File     : RunDictator.py

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from Dictator_ui import Ui_MainWindow
from glob import glob
import numpy as np
import json
from TimeLogger import TimeLogger

SAY_SOMETHING = {
    0: "Soldier, do something!",
    1: "Hm, still got a lot to do ~",
    2: "Oh, let's pick up them ASAP.",
    3: "Still in control~ Better watch out.",
    4: "Good! Keep going!",
    5: "Perfect! Why not try another round?"
}


class MainPanel(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainPanel, self).__init__()
        self.setupUi(self)
        self.logger = TimeLogger()

        self.source_directory_path = "resource/cfop/f2l"
        self.source_item_paths = []
        self.chosen_item_paths = []

        self.places = [self.Label1, self.Label2, self.Label3, self.Label4, self.Label5]
        self.alg_edits = [self.AlgEdit1, self.AlgEdit2, self.AlgEdit3, self.AlgEdit4, self.AlgEdit5]
        self.alg_results = [self.Result1, self.Result2, self.Result3, self.Result4, self.Result5]
        self.alg_answers = []
        self.chosen_indices = []

        self.ButtonRandom.setCursor(QCursor(Qt.PointingHandCursor))
        self.ButtonSubmit.setCursor(QCursor(Qt.PointingHandCursor))
        self.ButtonSubmit.setEnabled(False)

        self.ButtonRandom.clicked.connect(self.generateRandomSet)
        self.ButtonSubmit.clicked.connect(self.submit)

        self.setupSource()

    def setupSource(self):
        self.logger.info(msg="Start loading resources", start=True)
        self.source_item_paths = [p.replace('\\', '/') for p in sorted(glob(self.source_directory_path + '/*.png'))]
        with open("resource/cfop/solution.json", 'r') as f:
            self.solutions = json.load(f)["f2l"]

        for sip in self.source_item_paths:
            self.logger.debug(sip)

        self.logger.info(msg="Finish loading resources")

    def generateRandomSet(self):
        self.logger.info(msg="Start generating random set", start=True)
        self.reset_values()

        n_items = len(self.source_item_paths)
        if n_items > 5:
            indices = np.arange(n_items)
            np.random.shuffle(indices)
            self.chosen_indices = indices[:5]
            self.chosen_item_paths = [self.source_item_paths[i] for i in self.chosen_indices]
        else:
            self.chosen_item_paths = self.source_item_paths

        for sip, qlabel in zip(self.chosen_item_paths, self.places):
            self.logger.debug(msg="Load source image from {}".format(sip))
            qlabel.setPixmap(QPixmap(sip))

        chosen_algs = ["{:02d}".format(i + 1) for i in self.chosen_indices]

        self.logger.debug(msg="Test algorithms: {}".format(chosen_algs))
        self.logger.info(msg="Start generating random set")
        self.ButtonSubmit.setEnabled(True)

    def updateValues(self):
        self.alg_answers = [
            self.AlgEdit1.text(),
            self.AlgEdit2.text(),
            self.AlgEdit3.text(),
            self.AlgEdit4.text(),
            self.AlgEdit5.text()
        ]

    def reset_values(self):
        for qlabel, alg_edit, alg_result in zip(self.places, self.alg_edits, self.alg_results):
            qlabel.setStyleSheet("background-color: rgb(127, 127, 127);")
            alg_edit.setText("")
            alg_result.setText("NA")
            alg_result.setStyleSheet("color: rgb(0, 0, 0);")
        self.LabelSaySomething.setText("")

    def submit(self):
        self.logger.info(msg="Start analysing answerers", start=True)

        self.updateValues()
        chosen_algs = ["{:02d}".format(i + 1) for i in self.chosen_indices]
        self.logger.debug(msg="Load test algorithms: {}".format(chosen_algs))
        chosen_solutions = [self.solutions[alg] for alg in chosen_algs]
        self.logger.debug(msg="Load solutions: {}".format(chosen_solutions))

        n_correct = 0
        for i, (asw, sol, alg_result) in enumerate(zip(self.alg_answers, chosen_solutions, self.alg_results)):
            shorted_asw = asw.replace(' ', '').replace('(', '').replace(')', '')
            shorted_sol = sol.replace(' ', '').replace('(', '').replace(')', '')

            self.logger.debug(msg="Analyse situation {}".format(i))
            self.logger.debug(msg="Remove whitespaces, '(', ')' characters")
            self.logger.debug(msg="Shorted answer: {}".format(shorted_asw))
            self.logger.debug(msg="Shorted solution: {}".format(shorted_sol))

            if shorted_asw != shorted_sol:
                self.logger.debug(msg="Situation answer: FAIL!")
                alg_result.setText(sol)
                alg_result.setStyleSheet("color: rgb(255, 0, 0);")
            else:
                self.logger.debug(msg="Situation answer: PASS!")
                alg_result.setText('PASS')
                alg_result.setStyleSheet("color: rgb(0, 255, 0);")
                n_correct += 1

        self.LabelSaySomething.setText(SAY_SOMETHING[n_correct])
        self.logger.info(msg="Finish analysing answerers ({}/5)".format(n_correct))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main_panel = MainPanel()
    main_panel.show()
    sys.exit(app.exec_())
