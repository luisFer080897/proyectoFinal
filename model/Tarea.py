from dataclasses import dataclass, field

@dataclass
class Tarea:
    descripcion: str
    completada: bool = field(default=False)
 
    def marcar_completada(self) -> None:
        self.completada = True
 
    def desmarcar_completada(self) -> None:
        self.completada = False
 
    def toggle_completada(self) -> None:
        self.completada = not self.completada
 