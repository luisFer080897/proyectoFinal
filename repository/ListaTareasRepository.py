from typing import List
from model.Tarea import Tarea

class ListaTareasRepository:
    def __init__(self) -> None:
        self._tareas: List[Tarea] = []

    def agregar(self, descripcion: str) -> bool:
        descripcion = descripcion.strip()
        if not descripcion:
            return False
        self._tareas.append(Tarea(descripcion))
        return True

    def todas(self) -> List[Tarea]:
        return list(self._tareas)

    def obtener(self, indice_1_base: int) -> Tarea | None:
        idx = indice_1_base - 1
        if 0 <= idx < len(self._tareas):
            return self._tareas[idx]
        return None

    def completar(self, indice_1_base: int) -> bool:
        tarea = self.obtener(indice_1_base)
        if tarea:
            tarea.marcar_completada()
            return True
        return False

    def toggle(self, indice_1_base: int) -> bool:
        tarea = self.obtener(indice_1_base)
        if tarea:
            tarea.toggle_completada()
            return True
        return False

    def eliminar(self, indice_1_base: int) -> bool:
        idx = indice_1_base - 1
        if 0 <= idx < len(self._tareas):
            self._tareas.pop(idx)
            return True
        return False

    def eliminar_varios(self, indices_1_base: List[int]) -> int:
        """Elimina múltiples tareas. Retorna cuántas se eliminaron."""
        eliminadas = 0
        for idx in sorted(indices_1_base, reverse=True):
            if self.eliminar(idx):
                eliminadas += 1
        return eliminadas

    def limpiar(self) -> None:
        self._tareas.clear()

    def esta_vacia(self) -> bool:
        return len(self._tareas) == 0

    def total(self) -> int:
        return len(self._tareas)