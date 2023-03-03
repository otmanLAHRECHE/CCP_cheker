
import time
import PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

class ThreadLoadingApp(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self):
        super(ThreadLoadingApp, self).__init__()

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(100):
            self._signal.emit(i)
            time.sleep(0.007)
        self._signal_result.emit(True)


class ThreadLoadingVers(QThread):
    _signal = pyqtSignal(int)
    _signal_show = pyqtSignal(list)
    _signal_result_data = pyqtSignal(list)
    _signal_result = pyqtSignal(bool)

    def __init__(self, array):
        super(ThreadLoadingVers, self).__init__()
        self.array = array
        self.ret = []

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(len(self.array)):
            ligne = self.array[i]
            vers = []
            if(len(ligne)>0):
                rip = ligne[1:21]
                value = ligne[21:34]
                full_name = ligne[34:61]
                vers.append(full_name)
                vers.append(rip)
                value = int(value) / 100
                vers.append(value)
                self._signal_show.emit(vers)

                self.ret.append(vers)

            pors = i * 100
            pors = pors / len(self.array)
            self._signal.emit(pors)
            time.sleep(0.02)
        self._signal_result_data.emit(self.ret)
        self._signal_result.emit(True)


class ThreadLoadingCompte(QThread):
    _signal = pyqtSignal(int)
    _signal_show = pyqtSignal(list)
    _signal_result_data = pyqtSignal(list)
    _signal_result = pyqtSignal(bool)

    def __init__(self, array):
        super(ThreadLoadingCompte, self).__init__()
        self.array = array
        self.ret = []

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(len(self.array)):
            ligne = self.array[i]
            compt = []
            if(len(ligne)>0):
                rip = ligne[1:21]
                full_name = ligne[22:49]
                pas_thr = True
                for j in self.ret:
                    if(j[0] == full_name):
                        pas_thr = False
                
                compt.append(full_name)
                compt.append(rip)
                if(pas_thr):
                    compt.append("good")
                    self.ret.append(compt)
                else:
                    compt.append("dup")          
                
                self._signal_show.emit(compt)

                

            pors = i * 100
            pors = pors / len(self.array)
            self._signal.emit(pors)
            time.sleep(0.02)
        self._signal_result_data.emit(self.ret)
        self._signal_result.emit(True)


class ThreadScan(QThread):
    _signal = pyqtSignal(int)
    _signal_show = pyqtSignal(list)
    _signal_result_data = pyqtSignal(list)
    _signal_result = pyqtSignal(bool)

    def __init__(self, array_vers, array_compte):
        super(ThreadScan, self).__init__()
        self.array_vers = array_vers
        self.array_compte = array_compte
        self.ret = []

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        
        for i in range(len(self.array_vers)):
            verif = []
            vers = self.array_vers[i]
            test = False
            for j in range(len(self.array_compte)):
                compt = self.array_compte[j]
                if(vers[1] == compt[1]):
                    test = True
                    if(vers[0] == compt[0]):
                        vers.append("valide")
                    else:
                        vers.append("faut compte!!")
            
            if(test == False):
                vers.append("n'existe pas sur DB")
            
            self.ret.append(vers)
            
        
                    


        for i in range(len(self.array)):
            ligne = self.array[i]
            vers = []
            if(len(ligne)>0):
                rip = ligne[1:21]
                value = ligne[21:34]
                full_name = ligne[34:61]
                vers.append(full_name)
                vers.append(rip)
                value = int(value) / 100
                vers.append(value)
                self._signal_show.emit(vers)

                self.ret.append(vers)

            pors = i * 100
            pors = pors / len(self.array)
            self._signal.emit(pors)
            time.sleep(0.02)
        self._signal_result_data.emit(self.ret)
        self._signal_result.emit(True)
