import sys
from PyQt5 import QtWidgets
from repository.ListaTareasRepository import ListaTareasRepository
from ui.TareasApp import TareasApp
 
def main() -> None:
    app  = QtWidgets.QApplication(sys.argv)
    repo = ListaTareasRepository()
    ventana = TareasApp(repo)
    ventana.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()