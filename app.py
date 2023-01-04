import checking as chk
import smtplib
from email.message import EmailMessage
from tkinter import MULTIPLE
from segredos import password
from PySimpleGUI import PySimpleGUI as sg

#Configurar-email-senha
EMAIL_ADDRESS = 'tcgtestes@gmail.com'
EMAIL_PASSWORD = password


corpo_email = ''
assunto = ''


lista = []
msg = EmailMessage()
msg['From'] ='tcgtestes@gmail.com'


# Layout
sg.theme('Dark Blue 3')
layout = [
    [sg.Text('Logado com '+ EMAIL_ADDRESS)],
    [sg.Text('Para:'), sg.Input(key='email', size=(20,1)), sg.Button('Adicionar')],
    [sg.Text('Lista de emails:')],
    [sg.Listbox(lista,key='lista_email',enable_events=True,select_mode=MULTIPLE, size=(30,6)),sg.Button('Remover', button_color='Red', disabled=True)],
    [sg.Button('Limpar Lista')],
    [sg.Text('Assunto:'),sg.Input(key='assunto', size=(20,1))],
    [sg.Text('Mensagem:')], 
    [sg.Multiline(key='msg', size=(50, 8))],
    [sg.Button('Enviar')],
]

# Janela
janela = sg.Window('Enviar E-mails', layout)


def remove_button(selected_itens):
    if len(selected_itens) >= 1:
        # Coferindo os itens e removendo
        chk.double_list_check(selected_itens, lista)              
    # Update da ListBox
    janela['lista_email'].update(lista)


# Enviar um e-mail
def enviar_email():
    msg['Subject'] = assunto
    msg.set_content(corpo_email)
    msg['To'] = lista        
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)
        limpar_lista()
        limpar_campos()
        sg.popup('E-mails enviados!!')


# Resetar os campos 
def limpar_campos():
    janela['email'].update('')
    janela['assunto'].update('')
    janela['msg'].update('')


# Limpar a lista de emails
def limpar_lista():
    lista.clear()
    janela['lista_email'].update(lista)


# Atualiza a lista de emails
def atualizar_lista(email):

    # Verificando se o e-mail é válido
    padrao = chk.valid_email(email)

    # Checa se o email é válido
    if padrao:
        #   Checa se o item está na lista
        checked = chk.in_list_check(email, lista)
        if checked == False:
            lista.append(valores['email'])
            janela['lista_email'].update(lista)
            janela['email'].update('')
            print(lista)
        else:
            janela['email'].update('')
            sg.popup('Item já está na lista!!')
            
    else:
        sg.popup('[ERRO] \nDigite um email válido! \nEx:exemplo@email.com')


while True:
    eventos, valores = janela.read()    
    if eventos == sg.WIN_CLOSED:
        break

    # Remover da lista de e-mails
        # Listando os itens selecionados
    selected_itens = janela['lista_email'].get()
    if len(lista) >= 1 and len(selected_itens) >= 1:
        janela['Remover'].update(disabled=False)
    else:
        janela['Remover'].update(disabled=True)

    if eventos == 'Remover':
        remove_button(selected_itens)

    # Adicionar itens a lista de e-mails
    if eventos == 'Adicionar':
        if  valores['email'] != '':     
            atualizar_lista(valores['email'])
    
    # Enviar e-mails
    if eventos == 'Enviar':
        if len(lista) >= 1:
            assunto = valores['assunto']
            corpo_email = valores['msg']
            enviar_email()
        else:
            sg.popup('Por favor adicione emails a lista de envios!!')

    # Limpar a lista de emails
    if eventos == 'Limpar Lista':
        limpar_lista()
        
