1. Install virtualenv package for python by command:
	
	pip install virtualenv

2. Create new virtual enviroment by command:

	virtualenv env

3. Activate enviroment by command:
	
	env\Scripts\activate

4. Install all package we need to training by command:

	pip install -r requirements.txt

5. Training:
	
	# Train with daily dataset

	python eth_train.py

	# Train with realtime dataset

	python eth_train_v2.py