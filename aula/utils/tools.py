# This Python file uses the following encoding: utf-8

#----write pdf-------------------------------------
from django import http
from django.template.loader import get_template
from django.template import Context

import cStringIO as StringIO
import cgi
try:
    import ho.pisa as pisa
except:
    pass

#--------------------------------------------------

def getClientAdress( request ):
    
    return request.get_host()
    
#         #TODO:  HttpRequest.get_host()  at https://docs.djangoproject.com/en/dev/ref/request-response/
#     try:
#         FORWARDED_FOR_FIELDS = [
#             'REMOTE_ADDR',
#             'HTTP_X_FORWARDED_FOR',
#             'HTTP_X_FORWARDED_HOST',
#             'HTTP_X_FORWARDED_SERVER',
#         ]
#         for field in FORWARDED_FOR_FIELDS:
#             if field in request.META:
#                 if ',' in request.META[field]:
#                     parts = request.META[field].split(',')
#                     request.META[field] = parts[-1].strip()
#         client_address = request.META['HTTP_X_FORWARDED_FOR']
#     except:
#         client_address = request.META['REMOTE_ADDR']
#         
#     return client_address

def lowpriority():
    """ Set the priority of the process to below-normal."""

    pass
    
def getSoftColor( obj ):
    str = unicode( obj ) + u'con mucha marcha'
    i = 0
    j = 77
    for s in str:
        i += ( 103 * ord( s ) ) % 2001
        j = j % 573 + i * 5
    i = i*i
    
    gros = 200 + i%55
    mitja1 = 100 + j%155 
    mitja2 = 150 + (i+j)%105
    
    color=(None,None,None)
    if i%3 == 0:
        if i%2 ==0:
            color = ( gros, mitja1, mitja2 )
        else: 
            color = ( gros, mitja2, mitja1 )
    elif i%3 == 1:
        if i%2 ==0:
            color = ( mitja1, gros, mitja2 )
        else: 
            color = ( mitja2, gros, mitja1 )
    elif i%3 == 2:
        if i%2 ==0:
            color = ( mitja1, mitja2, gros )
        else:
            color = ( mitja2, mitja1, gros )
        
    return u'#{0:02X}{1:02X}{2:02X}'.format( color[0], color[1], color[2] )


def getImpersonateUser( request ):
    user = request.session['impersonacio'] if  request.session.has_key('impersonacio') else request.user
    l4 = request.session['l4'] if  request.session.has_key('l4') else False
    return ( user, l4, )

def getRealUser( request ):
    return request.user

def sessioImpersonada( request ):
    (user, _ ) = getImpersonateUser(request)
    return request and request.user.is_authenticated() and request.user.pk != user.pk

class classebuida(object):
    pass

class llista(list):
    def compte(self):
        return self.__len__()
    def __init__(self, *args, **kwargs):
        super(llista,self).__init__(*args,**kwargs)    

class diccionari(dict):
    def compte(self):
        return self.__len__()
    def itemsEnOrdre(self):
        return iter(sorted(self.iteritems()))
    def __init__(self, *args, **kwargs):
        super(dict,self).__init__(*args,**kwargs)    



def add_secs_to_time(timeval, secs_to_add):
    import datetime
    dummy_date = datetime.date(1, 1, 1)
    full_datetime = datetime.datetime.combine(dummy_date, timeval)
    added_datetime = full_datetime + datetime.timedelta(seconds=secs_to_add)
    return added_datetime.time()





def write_pdf(template_src, context_dict):
    
        
    template = get_template(template_src)
    #template = Template(filename = template_src, input_encoding = "utf-8")
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO( html.encode("utf-8")), dest=result, encoding='UTF-8', link_callback=fetch_resources)
    if not pdf.err:
        response = http.HttpResponse( result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=qualitativa.pdf'
    else:
        response = http.HttpResponse('''Gremlin's ate your pdf! %s''' % cgi.escape(html))

    
    return response

def fetch_resources(uri, rel):
    import os.path
    from django.conf import settings
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path


