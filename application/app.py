import re
import pyautogui as pa
import PySimpleGUI as sg
import web_scraping as wb

bws = wb.BookWebScraping()

sg.theme('Black')

layout = [ [sg.Text('Web Scraping Books')],
           [sg.Text('Email do Destinatário'), sg.Input(key='email', size=(25,1))],
           [sg.Button('Enviar')]]

window = sg.Window('Enviar Email', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Enviar':
        email = values['email']

        regex = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        if not bool( re.match( regex, email ) ):
            pa.alert('Escreva um email válido')

        else:
            #bws.receiver_email = email
            pa.alert('Iniciando o Web Scraping')
            pa.alert('Por Favor, aguarde')

            url = bws.url
            headers = bws.headers

            total_requests = bws.api_request( url=url, headers=headers )
            aux_link       = bws.get_links( total_requests )
            df_details     = bws.second_scrapy( aux_link )
            df_raw         = bws.save_scrapy( df_details )
    
            bws.send_email( sender_email=bws.sender_email, sender_pass=bws.sender_pass, receiver_email=email, df_raw=df_raw )

            pa.alert('Web Scrapinf Finalizado, Por favor, cheque o email: ' + str(email) )

window.close()
