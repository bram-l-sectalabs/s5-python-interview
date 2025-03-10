sudo cp /tmp/server* ./
python -m pip install pipenv --break-system-packages
python -m pip install -r requirements.txt --system-site-packages
python -m pipenv install
python -m pipenv shell