sudo cp /tmp/server* ./
python -m pip install pipenv --break-system-packages
python -m pipenv install
python -m pipenv shell
python -m pip install -r requirements.txt