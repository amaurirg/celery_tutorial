from time import sleep

from celery import Celery


# O primeiro argumento para Celeryé o nome do módulo atual.
# Isso só é necessário para que os nomes possam ser gerados automaticamente
# quando as tarefas são definidas no módulo __main__ .
# O segundo argumento é o argumento de palavra-chave do broker, especificando
# a URL do message broker que você deseja usar. Aqui estamos usando o RabbitMQ
# app = Celery('tasks', broker='pyamqp://guest@localhost//')


# Mantendo Resultados
# Se você quiser acompanhar os estados das tarefas, o Celery precisa armazenar
# ou enviar os estados para algum lugar.
# Para este exemplo, usamos o backend de resultado rpc , que envia estados de
# volta como mensagens transitórias.
app = Celery('tasks', backend='rpc://', broker='pyamqp://')

@app.task
def add(x, y):
    return x + y

# Agora você pode executar o trabalhador executando nosso programa com o worker argumento:
# celery -A tasks worker --loglevel=INFO


# Para chamar nossa tarefa, você pode usar o método delay().
# >>> from tasks import add
# >>> add.delay(4, 4)

# A tarefa agora foi processada pelo trabalhador que você iniciou anteriormente.
# Você pode verificar isso observando a saída do console do trabalhador.

@app.task
def soma(numero):
    for valor in range(10):
        add.delay(numero, valor)
        sleep(0.1)

# O método ready() retorna se a tarefa terminou o processamento ou não:
# result = add.delay(4, 4)
# result.ready()
# Você pode encontrar o id da tarefa observando o idatributo:
# >>> result.id

# Você pode esperar que o resultado seja concluído, mas isso raramente é usado,
# pois transforma a chamada assíncrona em uma síncrona ou inspecionar a exceção e rastrear se
# a tarefa gerou uma exceção, de fato result.get(), propagará quaisquer erros por padrão:
# result.get(timeout=1)

# Caso a tarefa tenha gerado uma exceção, a exceção get()será levantada novamente, mas
# você pode substituir isso especificando o argumento propagate:
# >>> result.get(propagate=False)
# Se a tarefa gerou uma exceção, você também poderá obter acesso ao traceback original:
# >>> result.traceback

# Se você não deseja que os erros se propaguem, você pode desabilitar isso passando propagate:
# >>> res.get(propagate=False)
# TypeError("unsupported operand type(s) for +: 'int' and 'str'")
# Nesse caso, ele retornará a instância de exceção levantada - então, para verificar se a tarefa
# foi bem-sucedida ou falhou, você terá que usar os métodos correspondentes na instância de resultado:
# >>> res.failed()
# True
#
# >>> res.successful()
# False
# Então, como ele sabe se a tarefa falhou ou não? Ele pode descobrir observando o estado das tarefas :
#
# >>> res.state
# 'FAILURE'
# Uma tarefa só pode estar em um único estado, mas pode progredir por vários estados.
# As etapas de uma tarefa típica podem ser:
#
# PENDING -> STARTED -> SUCCESS

# Para projetos maiores, um módulo de configuração dedicado é recomendado.
# Você pode dizer à sua instância Celery para usar um módulo de configuração chamando o
# método app.config_from_object():
# app.config_from_object('celeryconfig')
# Este módulo é frequentemente chamado de “ celeryconfig”, mas você pode usar qualquer nome de módulo.
# No caso acima, um módulo chamado celeryconfig.pydeve estar disponível para carregar no diretório atual
# ou no caminho do Python. Pode ser algo assim:
#
# celeryconfig.py:
#
# broker_url = 'pyamqp://'
# result_backend = 'rpc://'
#
# task_serializer = 'json'
# result_serializer = 'json'
# accept_content = ['json']
# timezone = 'Europe/Oslo'
# enable_utc = True

# Para verificar se seu arquivo de configuração funciona corretamente e não contém erros de sintaxe,
# você pode tentar importá-lo:
#
# $ python -m celeryconfig


# Para demonstrar o poder dos arquivos de configuração, é assim que você roteia uma tarefa com mau
# comportamento para uma fila dedicada:
# celeryconfig.py:
#
# task_routes = {
#     'tasks.add': 'low-priority',
# }
#
# Ou, em vez de roteá-lo, você pode limitar a taxa da tarefa, para que apenas 10 tarefas desse tipo
# possam ser processadas em um minuto (10/m):
# celeryconfig.py:
#
# task_annotations = {
#     'tasks.add': {'rate_limit': '10/m'}
# }
#
# Se você estiver usando RabbitMQ ou Redis como o broker, também poderá direcionar os trabalhadores
# para definir um novo limite de taxa para a tarefa em tempo de execução:
# $ celery -A tasks control rate_limit tasks.add 10/m
# worker@example.com: OK
#     new rate limit set successfully
