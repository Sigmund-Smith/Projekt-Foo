#funktioniert erst nach der erfolgreichen Ausführung von setup.sh

git pull

source python_umgebung/bin/activate
pip install -r requirements.txt # falls sich hier sachen geändert haben
python test.py # oder welches file auch immer am Anfang ausgeführt wird

deactivate
echo "Danke, dass sie sich die Zeit genommen haben"
