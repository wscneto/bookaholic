# Bookaholic

Bem-vindo ao Bookaholic, uma livraria online com microserviços.

Este projeto foi realizado como requisito da disciplina Engenharia de Software (ECOM021).

Professor: Dr. Arturo Hernández Domínguez

Equipe:

-   Pedro André da Silva Neto
-   Walter Soares Costa Neto

## Requisitos para executar o código

-   Python (3.12.3)
-   Node.js (v18.19.1)
-   npm (9.2.0)
-   MySQL (8.0.42)

Certifique-se de que possui essas tecnologias instaladas antes de executar o programa. As versões utilizadas durante o desenvolvimento estão explicitadas.

OBS.: O projeto utiliza usuário "root" e senha "root" para conectar-se com o banco de dados. Certifique-se de que a sua instalação do MySQL possui essas credenciais. Se quiseres alterar o usúario e senha utilizados, modifique o arquivo shared/db.py.

## Instruções

Para criar um ambiente virtual onde as bibliotecas de Python serão instaladas., execute:

```bash
python3 -m venv .venv
```

Para ativar o ambiente virtual, execute:

```bash
source .venv/bin/activate
```

Para instalar as bibliotecas, execute:

```bash
pip install -r shared/requirements.txt
```

Agora, execute o arquivo sql que criará o banco de dados e as tabelas:

```bash
mysql -u root -p < shared/setup_db.sql
```

Para inicializar os serviços, execute:

```bash
python3 start_services.py
```

Abra um novo terminal dentro da pasta do projeto.

Neste novo terminal, execute:

```bash
cd bookaholic-frontend/
npm run dev
```

O programa deve rodar em http://localhost:5173/
