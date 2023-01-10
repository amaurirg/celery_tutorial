from celery import Celery

app = Celery(
    'proj',
    broker='amqp://',
    backend='rpc://',
    include=['proj.tasks']
)

# Optional configuration, see the application user guide.
app.conf.update(
    task_routes={
        'proj.tasks.add': {'queue': 'fila'},
    },
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

# Neste módulo você criou nossa instância Celery (às vezes chamada de app ).
# Para usar o Celery em seu projeto, basta importar esta instância.
#
# O argumento broker especifica a URL do broker a ser usado.
#
# Consulte Escolhendo um corretor para obter mais informações.
#
# O argumento backend especifica o backend de resultado a ser usado.
#
# É usado para acompanhar o estado e os resultados da tarefa. Embora os resultados
# estejam desabilitados por padrão, eu uso o back-end de resultados RPC aqui porque
# demonstro como a recuperação de resultados funciona posteriormente. Você pode querer
# usar um back-end diferente para seu aplicativo. Todos eles têm diferentes pontos fortes
# e fracos. Se você não precisa de resultados, é melhor desativá-los. Os resultados também
# podem ser desabilitados para tarefas individuais definindo a @task(ignore_result=True)opção.
#
# Consulte Mantendo Resultados para obter mais informações.
#
# O includeargumento é uma lista de módulos a serem importados quando o trabalhador iniciar.
# Você precisa adicionar nosso módulo de tarefas aqui para que o trabalhador possa encontrar nossas tarefas.
