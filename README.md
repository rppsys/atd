# Laboratório de Testes em Python

Esse é um laboratório mínimo para testar os códigos em Python que estarei usando durante o curso de algotrading.

## Requisitos

> Ambiente Linux Ubuntu

Eu prefiro programar em Python no Ubuntu porque ele roda python nativo. 
Já programei python no Windows mas às vezes dá uma trabalheira 
principalmente quando ocorrem erros de codificação e aí é uma tristeza.
 
Se mesmo assim voê quiser usar o Windows faz o seguinte: 

    Roda o Ubuntu numa máquina virtual!
    
É sério, vai te poupar muito trabalho.  Baixa lá o:

https://www.virtualbox.org/

E instala o Ubuntu nele.    

## Instalação e Criação do Laboratório

Aqui vai uma passo-a-passo de como criar o laboratório no Ubuntu.

#### 1 - Abre seu terminal e digita:

    mkdir prog

Essa será sua pasta principal de programação. 

#### 2 - Instale agora o ambiente virtualenv

https://pythonacademy.com.br/blog/python-e-virtualenv-como-programar-em-ambientes-virtuais

Os comandos serão:

    sudo apt install python3-pip python-dev build-essential
    sudo pip3 install virtualenv virtualenvwrapper

#### 3 - Agora vamos criar um virtualenv para seu laboratório:

    python3 -m venv NOME_DO_VIRTUAL_ENV
    
Sugiro usar:
    
    python3 -m venv vATD

Eu crio um VirtualEnv para cada projeto e geralmente coloco a letra v seguido de 3 letras relacionadas ao projeto.

Como é algotrading, o nome pode ser vATD ou o que você quiser usar.

Ele cria o virtualenv.

Entre nele e ative-o:

    cd vATD
    
    source bin/activate
    
Ao ativar você verá que o terminal vai ficar assim:

    (vATD) user@user:
    
Pronto! Sempre que vc for trabalhar vc precisa entrar e ativar o Virtual Env.

#### 4 - Criar a pasta root

Se você entrar no vATD e digitar:

    ls
    
Você verá um monte de pastas e arquivos. Sempre que vc der um comando pip pra instalar algum pacote
do seu projeto, ele instalará os arquivos necessários desse pacote na pasta vATD.

Então, para organizar, dentro da pasta vATD eu sempre crio outra:

    mkdir rATD
    
A letra r vem de ROOT, ou seja, raiz. Essa é a pasta raiz onde vou criar todos os arquivos
do meu projeto. E aí, futuramente, quando eu precisar fazer bkp, eu copio só o conteúdo dessa
pasta.

No final sua pasta de trabalho será algo como:

    (vATD) user@User:~/prog/vATD/rATD$
    
É dentro desse rATD que vamos criar nossos códigos Python e etc.

#### 5 - Instalar o jupyter-notebook

O jupyter-notebook é uma forma muito interessante de fazer testes em Python pq ele 
permite escrever e rodar códigos direto no Browser.

https://jupyter.org/

https://jupyter.org/install.html

O comando que você digitará dentro da sua Virutal Env será:

    pip install jupyterlab
    
Aqui é importante instalar umas outras bibliotecas que iremos usar no laboratório:

    pip install pandas
    
    pip install matplotlib
    
    pip install bokeh
    
    bokeh sampledata
    
Pronto! Com isso aí o laboratório está quase pronto.
Vamos testa-lo.

## Usando o laboratório pela primeira vez

#### 1 - Rode o comando jupyter-notebook para abrir o jupyter:

    jupyter-notebook
    
Ele vai iniciar o jupyter e pedir pra vc abrir esse link. Abra-o:

http://localhost:8888

#### 2 - Crie seu primeiro ipynb

Vá em NEW e peça para criar seu primeiro Python3

Ele vai criar e haverá um quadro pra vc digitar o código Python

Para testar copie e cole esses comandos abaixo:

https://docs.bokeh.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart

    from bokeh.plotting import figure, output_file, show

    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    
    # output to static HTML file
    output_file("lines.html")
    
    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
    
    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)
    
    # show the results
    show(p)

O bokeh é um pacote que permite criar visualizações de dados em python. 

### Seu laboratório está criado! Explore as ferramentas e os link.




 

