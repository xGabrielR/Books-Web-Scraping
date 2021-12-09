import smtplib
import requests
import inflection

import pandas as pd

from email import encoders
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class BookWebScraping( object ):
    '''
    __(init)__
        - Set sender variables and requests.
    api_request
        - Start request at books.toscrape.
    first_scrapy
        - Collect showroom data at books.toscrape.
    get_links
        - Collect all products links.
    second_scrapy
        - With books links collect more data of books.
    save_scrapy
        - Save scrapy on a pandas dataframe.
    send_email
        - Send email to selected user.
    '''
    def __init__( self ):
        self.url = 'https://books.toscrape.com'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5),AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.sender_email = 'f0438iuj9r354hyu9f93@gmail.com'
        self.sender_pass  = '49UFH348Y8ygd7eq2gduy#'
        self.receiver_email = ''
        
    def api_request( self, url, headers ):
        page = requests.get( self.url, headers=self.headers )
        soup = BeautifulSoup( page.text, 'html.parser' )

        page_results = list( filter( None, soup.find( 'form', class_='form-horizontal' ).get_text().split('\n') ) )[0]
        total_products = int( page_results[0:4] )
        total_showcase = int( page_results[-3:-1] )
        total_requests = int( total_products / total_showcase)

        return total_requests

    def first_scrapy( self, total_requests ):
        aux_p = []
        aux_a = []

        for i in range( 1, total_requests+1 ): # Get all Price & Name Books.
            url_request = 'https://books.toscrape.com/catalogue/page-' + str(i) + '.html'

            page = requests.get( url_request, headers=self.headers )
            soup = BeautifulSoup( page.text, 'html.parser' )

            product_showcase = soup.find( 'ol', class_='row' )

            product_list = product_showcase.find_all('a', title=True)
            p_name = [p['title'] for p in product_list]
            aux_a.append( p_name )

            product_list = product_showcase.find_all( 'article', class_='product_pod' )
            product_list[1].find('p', class_='price_color').get_text()
            p_price = [p.find('p', class_='price_color').get_text().replace('Â£', '') for p in product_list]
            aux_p.append( p_price )

        p_price = []   # Array with all prices.
        for i in aux_p:
            for j in i:
                p_price.append( j )

        p_name = []
        for i in aux_a:
            for j in i:
                p_name.append( j )

        df_showcase = pd.DataFrame( [p_name, p_price] ).T
        df_showcase.columns = ['name', 'price']

        return df_showcase

    def get_links( self, total_requests ):
        aux_link = []
        for i in range( 1, total_requests+1 ): # Get all link info
            url_request = 'https://books.toscrape.com/catalogue/page-' + str(i) + '.html'

            page = requests.get( url_request, headers=self.headers )
            soup = BeautifulSoup( page.text, 'html.parser' )

            product_showcase = soup.find( 'ol', class_='row' )
            product_list = product_showcase.find_all('a', href=True)

            for i in range( 1, 40, 2 ):
                aux_link.append( product_list[i]['href'] )

        return aux_link 


    def second_scrapy( self, aux_link ):
        cols = ['upc', 'category', 'stock', 'price']
        df_details = pd.DataFrame()

        for i in aux_link:
            url  = 'https://books.toscrape.com/catalogue/' + i
            page = requests.get( url, headers=self.headers )
            soup = BeautifulSoup( page.text, 'html.parser' )

            #book_name
            p_name = soup.find('h1').get_text()

            #book_stock
            p_stock = int(list( filter( None, soup.find('p', 'instock availability').get_text().split('\n') ) )[1].replace(' ', '').replace('Instock(', '').replace('available)', ''))

            #book category
            p_category = list( filter( None, soup.find('ul', class_='breadcrumb' ).get_text().split('\n') ) )[2]

            #book_id
            product_table = soup.find('table', class_='table table-striped')
            p_upc = product_table.find('td').get_text()

            df_info = pd.DataFrame( [p_name, p_upc, p_category, p_stock] ).T
            df_info.columns = ['name', 'upc', 'category', 'stock']

            df_details = pd.concat( [df_details, df_info], axis=0 )

            return df_details

    def save_scrapy( self, df_showcase, df_details ):
        df_raw = pd.merge( df_showcase, df_details, on='name', how='left' ) # Join Dataframe
        df_raw['scrapy_datetime'] = datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ) # Save Scrapy datetime
        df_raw.to_csv( 'books.csv' ) # Save to CSV

        return df_raw

    def send_email( self, sender_email, sender_pass, receiver_email, df_raw ):
        email = '''Olá,
        Segue abaixo um anexo com a extração de dados
        do site books.toscrape.com as ''' + str(df_raw['scrapy_datetime'][0])

        sender_email = self.sender_email
        sender_pass  = self.sender_pass
        receiver_email = receiver_email

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To']   = receiver_email
        msg['Subject'] = 'Coleta de dados de Livros'

        msg.attach( MIMEText(email, 'plain') )
        attach_file = open( 'books.csv', 'rb' )

        pl = MIMEBase( 'application', 'octate-stream' )
        pl.set_payload( ( attach_file ).read() )
        encoders.encode_base64( pl )
        pl.add_header( 'Content-Disposition', "attachment; filename=books.csv" )
        msg.attach( pl )

        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login( self.sender_email, sender_pass) #login with mail_id and password
        text = msg.as_string()
        session.sendmail( sender_email, receiver_email, text)
        session.quit()

        return None

if __name__ == '__main__':
    bws = BookWebScraping()

    headers = bws.headers
    url = bws.url

    sender_email = bws.sender_email
    sender_pass  = bws.sender_pass
    receiver_email = ''
    
    total_requests = bws.api_request( url, headers )
    aux_link = bws.get_links( total_requests )
    
    df_showcase = bws.first_scrapy( total_requests )
    df_details  = bws.second_scrapy( aux_link )
    df_raw = bws.save_scrapy( df_showcase, df_details )
    
    bws.send_email( sender_email, sender_pass, receiver_email, df_raw )