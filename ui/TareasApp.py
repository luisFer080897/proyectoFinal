from PyQt5 import QtWidgets, QtCore, QtGui
from repository.ListaTareasRepository import ListaTareasRepository
from model.Tarea import Tarea
 
# 3) Widget personalizado para cada fila de tarea
class TareaItem(QtWidgets.QListWidgetItem):
    """Representa visualmente una Tarea en el QListWidget."""
 
    ICONO_PENDIENTE   = "⏳"
    ICONO_COMPLETADA  = "✔"
 
    def __init__(self, tarea: Tarea) -> None:
        super().__init__()
        self.tarea = tarea
        self._actualizar_texto()
 
    def _actualizar_texto(self) -> None:
        icono = self.ICONO_COMPLETADA if self.tarea.completada else self.ICONO_PENDIENTE
        self.setText(f"{icono}  {self.tarea.descripcion}")
 
    def refrescar(self) -> None:
        """Llama a esto tras cambiar el estado de la tarea."""
        self._actualizar_texto()
 
 
# 4) Ventana principal de la aplicación
class TareasApp(QtWidgets.QWidget):
    """Interfaz gráfica para gestionar la lista de tareas."""
 
    TITULO = "Lista de Tareas"
 
    def __init__(self, repositorio: ListaTareasRepository) -> None:
        super().__init__()
        self._repo = repositorio
        self._configurar_ventana()
        self._crear_widgets()
        self._crear_layout()
        self._conectar_signals()
 
    # ------------------------------------------------------------------
    # Configuración inicial
    # ------------------------------------------------------------------
    def _configurar_ventana(self) -> None:
        self.setWindowTitle(self.TITULO)
        self.resize(460, 400)
 
    def _crear_widgets(self) -> None:
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Escribe la descripción de la tarea...")
 
        self.btnAgregar   = QtWidgets.QPushButton("➕ Agregar")
        self.btnCompletar = QtWidgets.QPushButton("✔ Completar")
        self.btnEliminar  = QtWidgets.QPushButton("🗑 Eliminar")
        self.btnLimpiar   = QtWidgets.QPushButton("🧹 Limpiar todo")
 
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
 
        self.lblContador = QtWidgets.QLabel("Tareas: 0")
 
    def _crear_layout(self) -> None:
        filaEntrada = QtWidgets.QHBoxLayout()
        filaEntrada.addWidget(self.input)
        filaEntrada.addWidget(self.btnAgregar)
 
        filaBotones = QtWidgets.QHBoxLayout()
        filaBotones.addWidget(self.btnCompletar)
        filaBotones.addWidget(self.btnEliminar)
        filaBotones.addWidget(self.btnLimpiar)
 
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(filaEntrada)
        layout.addWidget(self.listWidget)
        layout.addLayout(filaBotones)
        layout.addWidget(self.lblContador)
 
    def _conectar_signals(self) -> None:
        self.btnAgregar.clicked.connect(self._on_agregar)
        self.btnCompletar.clicked.connect(self._on_completar)
        self.btnEliminar.clicked.connect(self._on_eliminar)
        self.btnLimpiar.clicked.connect(self._on_limpiar)
        self.input.returnPressed.connect(self._on_agregar)
 
    # ------------------------------------------------------------------
    # Slots (manejadores de eventos)
    # ------------------------------------------------------------------
    def _on_agregar(self) -> None:
        descripcion = self.input.text().strip()
        if not descripcion:
            self._aviso("Escribe una descripción.")
            return
 
        if self._repo.agregar(descripcion):
            tarea = self._repo.todas()[-1]
            item = TareaItem(tarea)
            self.listWidget.addItem(item)
            self.input.clear()
            self.input.setFocus()
            self._actualizar_contador()
 
    def _on_completar(self) -> None:
        filas = self._filas_seleccionadas()
        if not filas:
            self._aviso("Selecciona al menos una tarea.")
            return
 
        for fila in filas:
            self._repo.toggle(fila + 1)          # +1: índice base-1
            item: TareaItem = self.listWidget.item(fila)
            item.refrescar()
 
    def _on_eliminar(self) -> None:
        filas = self._filas_seleccionadas()
        if not filas:
            self._aviso("Selecciona al menos una tarea.")
            return
 
        eliminadas = self._repo.eliminar_varios([f + 1 for f in filas])
 
        # Eliminar de la vista de mayor a menor para no desfasar índices
        for fila in sorted(filas, reverse=True):
            self.listWidget.takeItem(fila)
 
        self._actualizar_contador()
        self._aviso(f"Se han eliminado: {eliminadas} tareas.")
 
    def _on_limpiar(self) -> None:
        if self._repo.esta_vacia():
            self._aviso("La lista ya está vacía.")
            return
 
        if self._confirmar("¿Eliminar TODAS las tareas?"):
            self._repo.limpiar()
            self.listWidget.clear()
            self._actualizar_contador()
 
    # ------------------------------------------------------------------
    # Helpers de UI
    # ------------------------------------------------------------------
    def _filas_seleccionadas(self) -> list[int]:
        return [idx.row() for idx in self.listWidget.selectedIndexes()]
 
    def _actualizar_contador(self) -> None:
        self.lblContador.setText(f"Tareas: {self._repo.total()}")
 
    def _aviso(self, mensaje: str) -> None:
        QtWidgets.QMessageBox.information(self, "Aviso", mensaje)
 
    def _confirmar(self, pregunta: str) -> bool:
        resp = QtWidgets.QMessageBox.question(
            self, "Confirmar", pregunta,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        return resp == QtWidgets.QMessageBox.Yes
 