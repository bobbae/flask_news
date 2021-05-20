git clone git@w10.gitlab.com:sadasystems/Training/dataeng-session-1-2020


because in .ssh/config:

Host gitlab
    User bobbae
    Port 22
    Hostname gitlab.com
    IdentityFile ~/.ssh/id_rsa

Host w10.gitlab.com
    User bobbaesada
    Port 22
    Hostname gitlab.com
    IdentityFile ~/.ssh/id_rsa_w10
