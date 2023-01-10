from .celery import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

# Iniciando o trabalhador (worker)
# O programa aipo pode ser usado para iniciar o trabalhador (você precisa
# executar o trabalhador no diretório acima do proj):
# $ celery -A proj worker -l INFO

# Chains
# As tarefas podem ser vinculadas para que, após o retorno de uma tarefa, a outra seja chamada:
#
# >>> from celery import chain
# >>> from proj.tasks import add, mul
#
# # (4 + 4) * 8
# >>> chain(add.s(4, 4) | mul.s(8))().get()
# 64
# ou uma cadeia parcial:
#
# >>> # (? + 4) * 8
# >>> g = chain(add.s(4) | mul.s(8))
# >>> g(4).get()
# 64
# As cadeias também podem ser escritas assim:
#
# >>> (add.s(4, 4) | mul.s(8))().get()
# 64
