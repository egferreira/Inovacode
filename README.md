# Cardeal Assist (programa construído para o Hackathon InovaCode 2020)

## Descrição

O Cardeal Assist é uma assistente pessoal para ajudar em produtividade no trabalho ou estudos, permitindo a divisão melhor entre vida pessoal e profissional. Assim, sincronizada com a Google Agenda atráves da API do Google, ela permite o agendamento de tarefas, assistente de foco utilizando a técnica pomodoro bem como o bloqueio de sites de redes sociais ou da preferência do usuário durante o período de foco. Além disso, o sistema permite a bonificação pela conclusão de tarefas ou tempo de trabalho, gamificando a solução e permitindo a migração do regime de trabalhos por carga horária para o regime de produtividade.    

### Informações gerais
- Os scripts principais estão na pasta "/scripts", onde o "main.py" é responsável por iniciar as threads principais para executar as funções descritas

- Interface básica para criação de tarefas com prioridades
![Alt text](/docs/Aplicacao3.png?raw=true "Basic Interface")

- Especificação de perídos de trabalho no Google Agenda
![Alt text](/docs/cardeal1.png?raw=true "Google Agenda Interface")

- Agendamento automático de acordo com prioridades e duração de tarefas, em relação ao períodos previamente especificados
![Alt text](/docs/cardeal2.png?raw=true "Google Agenda Interface")

## Features
- Integração com Google Agenda para definição de períodos de trabalho
- Interface visual para escrita das tarefas, com campos de tempo necessário para realizar a tarefa (em minutos) e a prioridade da tarefa (quanto maior, mais prioritária)
- Auto-agendamento dos períodos de trabalho em relação às tarefas, utilizando os tempos pré-definidos e ordenando segundo as prioridades
- Utilização da técnica pomodoro e bloqueio de sites que levam a distrações, aumentando o coeficiente de produtividade durante o período
- Verificação automática de recompensas de acordo com quantidade e tempo de tarefas concluídas

## Disclaimer
- Para a utilização, é necessária a autorização via API do Google Agenda, por meio de confirmação no site e download do "credentials.json", o qual deve ser colocado no diretório "/config/", na mesma hierarquia do diretório "/scripts/"

## To do (next steps)
- Adicionar sugestões de sáude
- Gerar aplicativo móvel
- Análise de períodos de maior produtividade, com alocação melhor do tempo para diversos tipos de tarefas
- Ferramenta de gestão para análise de performance pela gerência
- União com metas individuais e coletivas
- Aprimorar análise de recompensas e metas
- Adicionar lembrete de alimentação e análise de sono
