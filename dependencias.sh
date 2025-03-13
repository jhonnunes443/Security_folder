sudo apt install python3 -y
sudo apt update  -y && sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "[+] Caso de ocorra algum erro tire as permissões de root da pasta!"
echo "sudo chown -R user:user Security_folder"
