# Dieses file geht davon aus, dass das projekt schon geclont wurde und man sich in diesem Ordner befindet

# hier wird der selbst geschriebene code aktualisiert
git pull
 
#ein order wird erstellt
mkdir python_umgebung

# eine virtuelle python umgebung wird erstellt
python3 -m venv python_umgebung

# die virtuelle python umgebung wird gestartet
source python_umgebung/bin/activate

# die benötigten python module werden installiert
pip install -r requirements.txt

# ab hier kann die magie beginnen
echo " \n Herzlichen glückwunsch :) \n jetzt muss nurnoch start.sh gestartet werden und es kann losgehen
