# USA ESTE ARCHIVO PARA REALIZAR PRUEBAS DE COSAS QUE NO ESTES SEGUR@ DE PYTHON
import pickle, yaml

ola = "texto"
print(ola)
ola = pickle.dumps(ola)
print(ola)
print(pickle.loads(ola))

#8 de la tarea de Jose Luis
"""
SELECT *, COUNT()
FROM Estudiantes
WHERE ID_Estudiante < 5
"""