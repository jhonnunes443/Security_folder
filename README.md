#INSTALE AS DEPENDÊNCIAS DO PYTHON 

#DÊ AS PERMISSÕES PARA A PASTA DO PROJETO

sudo chown -R user:user Security_folder


$pip install -r requirements.txt

#USE O ARQUIVO PYTHON PARA FAZER O REVERSE SHELL, CONFIGURE NO ARQUIVO O EXATO IP E PORTA ONDE
ESTARÁ ESCUTANDO NA SUA MAQUINA;

#VOCÊ PODE USAR A OPÇÃO 'help' NO TERMINAL PARA VER ALGUMAS FUNCIONALIDADES DO SCRIPT;

##########
Manual:
-[help or -h] - Open the manual code;

-[execute] - to execute commands with a message returned for you;

-[cd or Cd] - to change directory;

-[cls or clear] - to clean the terminal;

-[ls or dir] - to list files;

-[info_ip] - to see IP addresses.

-[Download] - Download mode for files from the server(make shure you are using the client.py file to connect on 8887 port);

-[Upload] - to upload files from your computer(make shure you are using the server.py listening on 8889 port and the same address).

-[nmap_install] - Nmap installation for ip addresses scan.

-[quit] - Exit.

##########

#NA PASTA "reverse_shell" VOCÊ VERÁ ALGUNS O ARQUIVO "comunication.py"  ELE É O SEU ARQUIVO PARA INICIALIZA O SERVIDOR OU FAZER
CONEXÃO COM O SERVIDOR ONDE VOCê IRÁ FAZER ENVIO DA PASTA NA QUAL VOCÊ QUER ENVIAR ZIPADA PARA O CLIENTE;

###############

MENU PANEL USAGE:

1. Activate Server on 8887 port;
2. Activate Client on 8889 port;
3. Netcat installation;
4. Setup of your reverse shell ip and port;
5. Become executable;
6. Exit.

###############

Choose: 

#QUANDO CONECTADOS O CLIENTE DEVERÁ DIZER O NOME DA PASTA QUE SERÁ 
ENVIADA DO SERVIDOR, ELE IRÁ EXECUTAR A LÓGICA VERIFICAR SE EXISTE O ARQUIVO E FAZER O ENVIO.

#NA PASTA MALWARE ESTÃO MEUS MAIS RECENTES PROJETOS ATUALIZADOS ONDE O ARQUIVO "malware.py" É UMA JUNÇÃO DOS MEUS ULTIMOS PROJETOS 
DE REVERSE_SHELL + KEYLOGGER, USE O ARQUIVO "doorman.py" PARA CONFIGURAR TODOS OS IPS, PORTAS E INFORMAÇÕES DE EMAIL, SENHA E DESTINO
DE EMAIL. 

doorman.py:

###############

MENU PANEL USAGE:

1. Activate Server on 8887 port;
2. Activate Client on 8887 port;
3. Netcat installation;
4. Setup of your reverse shell ip and port;
5. Become executable;
6. Exit.

###############

#AO EXECUTAR O "malware.py" VOCÊ EXECUTARÁ O KEYLOGGER QUE IRÁ CAPTURAR TODAS AS TECLAS DE UM TECLADO E TENTAR ENVIAR POR EMAIL 
CASO SUAS CREDENCIAIS ESTEJAM CORRETAS, NO ENTANTO SE NÃO ESTIVEREM ELE CRIA UM ARQUIVO "settings1.txt"  ONDE VOCÊ TERÁ O CONTEÚDO 
DAS TECLAS E IPS COMO PROVEDOR, IP PÚBLICO, ETC...

#NÃO SE ESQUEÇA DE CONFIGURAR O TEMPO QUE ELE CAPTURA AS TECLAS NO ARQUIVO "doorman.py" OU NO CÓDIGO DO SCRIPT.




creditos: Jhean Phabio Silva Santos
