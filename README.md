# Covid_Datasus
Importante adicionar o Winrar a variavel de ambiente path do windows para funcionar a extração correta do arquivo .rar.
Como a ideia era desenvolver um script totalmente independente de interação humana, fiz de uma forma que ele se atualiza sozinho, e para isso precisei realizar algumas tarefas como:

O primeiro bloco de código foi feito para deletar a pasta que contém os CSV's, pois como ele roda todo dia, se não fizer isso, a pasta iria ficar cheia de CSV's antigos, o que iria encher a memória de armazenamento, sendo assim, toda vez que roda o código, ele deleta o diretorio no meu caso "covid_csvs", e no terceiro bloco de código ele cria novamente o diretorio "covid_csvs" para receber os CSV's extraidos.

O segundo bloco de código é responsável pela atualização da url que contém o arquivo rar, ou seja, a primeira requisição entra no link fixo que trás um Json com algumas informações, e entre elas vem a URL que contém o arquivo .rar onde eu faço uma mineração de string para trazer essa URL e armazenar na variavel "url2" que vamos usar para extrair os CSV's

O terceiro bloco de código é responsável por baixar o arquivo .rar fazendo uma requisição na URL2, após baixar ele faz a extração dos CSV's e armazena no diretório criado no final do caminho, no meu caso "covid_csvs"

Feito esses três passos, os arquivos CSV's já estão armazenados no seu PC, e você pode carrega-los para o jupyter, porém como eu fiz para ser auto atualizado, eu realizei algumas tarefas no quarto e quinto bloco, a fim de puxar o dia, o mês e o ano atualizado, para quando for importar os CSV's ele fazer isso atualizado conforme o dia, mês e ano corretos, pois a URL atualiza todo dia, e vem com a data no seu nome. Então mineirei o dia, mês e ano no quarto bloco, e no quinto eu fiz uma validação de sábado e domingo, pois o governo só atualiza a base de segunda a sexta, então se você rodar o código no sábado e domingo iria quebrar o código, e por isso decidi fazer essa validação, sempre que o código for executado no sabado o script vai entender o dia como dia -1 e se for no domingo ele entende dia - 2, e assim fica auto atualizavel.

No próximo bloco eu faço a importação dos CSV's, e atribuo as variaveis, para que no bloco seguinte seja feita a concatenação dos dataframes, pois eu queria deixar um só no final, e não 6 como vem nos CSV's.

Após deixar um dataframe só, eu dropo algumas colunas que não me interessam, ai no caso a análise é de cada um.

E o último bloco eu faço o envio do dataframe para uma tabela no MySQL, onde posso conectar com o Power B.I por exemplo para fazer a parte de visualização de dados, e ai você que decide se manda para um banco de dados, ou se gera um novo CSV ou Parquet etc...
Lembrando que toda vez que o código é executado esse ultimo bloco faz sobreescrever os dados no MySQL para não ter duplicidade dos dados.

E para finalizar, eu usei o agendador de tarefas do Windows para automatizar a execução do script, programei para uma vez por dia o Windows rodar automaticamente meu script, onde faz a atualização dos dados no meu BD, finalizando com sucesso a minha ideia de criar um código totalmente automatizado, sem precisar ter a interação humana.
