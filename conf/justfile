alias si := system-info

system-info:
    @echo from ~/justfile
    @echo "This is an {{arch()}} machine running {{os()}}".
    @echo PATH is {{env_var("PATH")}}
    # the same as @echo PATH is $PATH
    @echo current invocation directory is {{invocation_directory()}}

ssh-host-keys:
	sudo ssh-keygen -b 1024 -t rsa -f /etc/ssh/ssh_host_key
	sudo ssh-keygen -b 1024 -t rsa -f /etc/ssh/ssh_host_rsa_key 
	sudo ssh-keygen -b 1024 -t dsa -f /etc/ssh/ssh_host_dsa_key

sshd-start:
	sudo service ssh start

ngrok-ssh-start:
	ngrok tcp 22

add-sudoers:
	echo bob     ALL=(ALL:ALL) NOPASSWD:ALL | sudo tee -a /etc/sudoers

file-server:
	deno run --allow-net --allow-read https://deno.land/std/http/file_server.ts

asdf-sbcl:
	# asdf list
	# asdf plugin add sbcl
	asdf install sbcl 2.0.4
	# asdf current
	asdf global sbcl 2.0.4

get-rush:
	# gnu parallel alternative
	go get -u github.com/shenwei356/rush/

will-cite-parallel:
	echo 'will cite' | parallel --citation 1> /dev/null 2> /dev/null &

one-click-hugo-run:
	# yarn
	npx yarn start
	# git push origin master

flask-news-update:
	git push heroku master
	# git push origin master

heroku-database:
	export DATABASE_URL=`heroku config:get DATABASE_URL -a aaa12w3 -j`

create-venv:
	python3 -m venv ~/venv-some-dir

venv-jupyter:
	source /home/bob/venv-jupyter/bin/activate

create-requirements:
	pip freeze > requirements.txt

clean-requirements:
	pipreqs --force .

