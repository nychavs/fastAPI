from typing import Optional
from fastapi import FastAPI, Response, Path
from fastapi import HTTPException, status
from models import Curso


app = FastAPI()

cursos = {
    1: {
        "nome" : "python",
        "aulas":20,
        "horas":80,
        "instrutor":"Cleber"
    },
    2: {
        "nome":"Java",
        "aulas":15,
        "horas":60,
        "instrutor":"Leonardo"
    }
}
@app.get('/cursos')
async def get_cursos():
    return cursos
    
@app.get('/cursos/{curso_id}')
async def get_cursos(curso_id: int = Path(default=None, title='ID do Curso', description='Deve estar entre 1 e 2', gt=0, lt=3)):
    try:
        curso = cursos[curso_id]
        curso.update({"id":curso_id})
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id = len(cursos)+1
    if curso.id not in cursos:
        cursos[next_id] = curso
        return curso
    else: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"ja existe um curso com o id {curso.id}")

@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse curso não existe.")

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse Curso Não existe")

@app.get('/calculadora')
async def get_numeros(a: int=Query(default=None, gt=5), b: int = Query(default=None, gt=5), x_test: str = Header(default=None), c: Optional[int] = 0):
    soma = a + b + c
    print(f'X_TEST: {x_test}')
    return soma

if __name__=='__main__':
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level='info', reload=True)
