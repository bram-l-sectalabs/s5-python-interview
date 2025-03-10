sudo cp /tmp/secrets* ./
python -m pip install pipenv --break-system-packages
python -m pipenv install
python -m pipenv shell
