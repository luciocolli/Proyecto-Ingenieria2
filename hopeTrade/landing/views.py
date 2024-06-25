from django.shortcuts import render, redirect, get_object_or_404
from .models import Publication, Offer, CashDonation, Coment, Intercambio, ArticleDonation, Calification
from django.db import IntegrityError
from users.models import User, Card
from .forms import CreateNewPublication, EditPublicationForm, cashRegisterForm, ComentPublicationForm, CreateNewOffer, articleRegisterForm, calificationForm
from django.contrib.auth.decorators import login_required, admin_required
from users.views import editarPerfil #Sin uso era para ver si se solucionaba
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum
from users import backend as back
from datetime import date
# Create your views here.


def index(request):
    return render(request, 'base.html')


def about(request):
    return render(request, 'about.html')


@login_required
def createPublication(request):


    # def exists_title(user, title):
    """
    Esta función debe verificar que el usuario no contenga publicaciones 
    actuales con el nombre recibido, pero si puede contener intercambios
    realizados con ese nombre
    """
    #     try: 
    #         # Tomo las publicaciones del usuario que no se encuentran en ningún intercamvbi
    #         post = Publication.objects.all(user=user, title= title, isHide= False)
        

    if request.method == 'GET':
        return render(request, 'createPublication.html', {
            'form': CreateNewPublication()
        })
    else:
        # publication = Publication.objects.get(id=1)
        # publication.delete()

        form = CreateNewPublication(request.POST)

        if form.is_valid():

            new_title = request.POST['title']
            post_owner = request.user
            exists_title = Publication.objects.filter(user= post_owner, title= new_title).exists()
            cleaned_date = form.cleaned_data['date'] # The date is cleaned in case it's empty
            # This conditional checks if the user that is creating the post already has one with the same title
            if exists_title:
                # In this case, the user is notified
                form.add_error(
                        'title', 'Ya posees una publicación con este título'
                        )
                return render(request, 'createPublication.html', {'form': form})
            else:
                Publication.objects.create(
                    title=request.POST['title'],
                    description=request.POST['description'],
                    category=request.POST['category'],
                    state=request.POST['state'],
                    date=cleaned_date,
                    user=request.user,  # esto retorna al usuario que se encuentra navegando en el sistema
                    file= request.POST['file']
                )
                return redirect('all-posts')
        else:
            return render(request, 'createPublication.html', {'form': form})

@login_required
def editPublication(request, publication_id):

    publication = get_object_or_404(Publication, id=publication_id)
    mensaje = None

    def hasOffers(user):
        return Offer.objects.exists(user)
    
    def title_exists(new_title):
        return Publication.objects.filter(user = publication.user, title = new_title).exclude(id=publication.id).exists()

    def guardar_form():
        form.save()
        return 'Se han guardado los cambios correctamente'

    
    # Verifica si el usuario logueado es el creador de la publicación
    if publication.user != request.user and not hasOffers(publication.user):
        mensaje = "No tienes permiso para editar esta publicación."

    if request.method == 'POST':
        form = EditPublicationForm(request.POST, instance=publication)
        if form.is_valid():
            if not title_exists(form.cleaned_data['title']):
                mensaje =  'Se han guardado los cambios correctamente'

                if form.cleaned_data['category'] != 'alimento':
                    publication.date = None
                    mensaje = guardar_form()
                elif form.cleaned_data['date'] == None:
                    mensaje = 'Debes ingresar una fecha de vencimiento'
                elif form.cleaned_data['date'] < date.today():
                    mensaje = 'No puedes ingresar productos vencidos'
                else:
                    guardar_form()
                
            else:
                mensaje = "Ya posees una publicación con este título"
    else:
        form = EditPublicationForm(instance=publication)
    return render(request, 'editPublication.html', {
        'form': form,
        'mensaje': mensaje
    })

@login_required
def show_all_posts(request):
    if request.method == 'GET':
        logged_user = request.user
        categories = request.GET.getlist('category')
        search = request.GET.get('search', '')

        # Empezar con todas las publicaciones que no sean del usuario actual
        posts = Publication.objects.exclude(user=logged_user).filter(isHide = False)

        if categories:
            # Filtrar publicaciones por categorías seleccionadas
            posts = posts.filter(category__in=categories)

        if search:
            # Filtrar publicaciones por título
            search_words = search.split()
            for word in search_words:
                posts = posts.filter(title__icontains=word)

        # Mensaje de resultados
        if not posts:
            if categories and search:
                message = f'No hay publicaciones disponibles para la(s) categoría(s) "{", ".join(categories)}" con el título "{search}"'
            elif categories:
                message = f'No hay publicaciones disponibles para la(s) categoría(s): {", ".join(categories)}'
            elif search:
                message = f'No hay publicaciones disponibles con el título "{search}"'
            else:
                message = 'No hay publicaciones disponibles'
        else:
            message = None

        return render(request, 'show-all-posts.html', {
            'nombre_usuario': logged_user.name,
            'posts': posts,
            'msg': message
        })

@login_required
def show_my_profile(request):

    if request.method == 'GET':
        logged_user = request.user
        # logged_user = get_object_or_404(User.objects.filter(id=2))
        dni = logged_user.dni
        return render(request, 'miperfil.html', {
            'dni' : dni,
            'name' : logged_user.name,
            'surname' : logged_user.surname,
            'mail' : logged_user.mail,
            'date' : logged_user.date
        })

@login_required  #Para ver Publicacion en la pagina principal
def show_post(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Publication, id=id)
        return render(request, 'view-post.html', {
            'title': post.title,
            'description': post.description,
            'category': post.category,
            'state': post.state,
            'date': post.date,
            'user': post.user,
            'file' : post.file,
            'id' : post.id,
            'form' : ComentPublicationForm(),
            'post_id': int(post.id)
        })

def show_my_posts(request): # Para ver listado de mis publicaciones
    if request.method == 'GET':
        logged_user = request.user
        myPosts = Publication.objects.filter(user=logged_user)

        if not myPosts:
            message = 'No hay publicaciones disponibles'
        else:
            message = None

        return render(request, 'my-posts.html',{
            'myPosts' : myPosts,
            'msg': message
        })

@login_required
def show_my_post(request, id):  # Para ver una publicacion propia
    if request.method == 'GET':
        post = get_object_or_404(Publication, id=id)
        return render(request, 'view-my-post.html', {
            'title': post.title,
            'description': post.description,
            'category': post.category,
            'state': post.state,
            'date': post.date,
            'file': post.file,
            'id' : post.id
        })
    
#@admin_required
def admin_posts(request):   
    if request.method == 'GET':
        categories = request.GET.getlist('category')
        search = request.GET.get('search', '')

        if categories:
            # Filtrar publicaciones por categorías seleccionadas
            posts = Publication.objects.filter(category__in=categories) 
            if not posts:
                # Si no hay publicaciones para las categorías seleccionadas, mostrar mensaje
                message = f'No hay publicaciones disponibles para la(s) categoría(s): {", ".join(categories)}'
            else:
                message = None
        else:
            # Mostrar todas las publicaciones (excepto las del usuario)
            posts = Publication.objects.all()
            if not posts:
                # Si no hay publicaciones en el sistema, mostrar mensaje
                message = 'No hay publicaciones disponibles'
            else:
                message = None

        if search:
            # Filtrar publicaciones por título
            search_words = search.split()
            for word in search_words:
                posts = posts.filter(title__icontains=word)

        # Mensaje de resultados
        if not posts:
            if categories and search:
                message = f'No hay publicaciones disponibles para la(s) categoría(s) "{", ".join(categories)}" con el título "{search}"'
            elif categories:
                message = f'No hay publicaciones disponibles para la(s) categoría(s): {", ".join(categories)}'
            elif search:
                message = f'No hay publicaciones disponibles con el título "{search}"'
            else:
                message = 'No hay publicaciones disponibles'
        else:
            message = None

        return render(request, 'admin-show-posts.html', {
            'posts': posts,
            'msg': message
        })
    else:
        posts = Publication.objects.all()
        return render(request, 'admin-show-posts.html', {
            'posts': posts
        })

#COMENTO XQ NO ME FUNCIONA (RAMI)
#@admin_required
def delete_post(request, id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publication, id=id)
        back.enviarMail(publicacion.user.mail,'Publicación eliminada', f'Hola {publicacion.user.name}, tu publicación {publicacion.title} ha sido eliminada porque era indebida.')
        
        # si la publicacion esta escondida es por que tiene una oferta aceptada pero no el intercambio confirmado
        # le avisamos al ofertador que se elimino la publicacion para que no vaya la centro de caritas
        if publicacion.isHide:
            intercambio = Intercambio.objects.get(post = publicacion)
            ofertador = intercambio.offerOwner
            back.enviarMail(ofertador.mail,'Publicación eliminada', f'Hola {ofertador.name}, la publicación {publicacion.title} en la que realizaste una oferta ha sido eliminada porque era indebida.')
        
        publicacion.delete()
        posts = Publication.objects.all()
        return render(request, 'admin-show-posts.html', {
            'posts': posts
        })

@login_required
def donation(request):
    donations = CashDonation.objects.all()
    total_donations = CashDonation.objects.aggregate(total= Sum('cash'))['total']
    return render(request, 'donation.html',{
        'donations' : donations,
        'total_donations' : total_donations
    })

@login_required
def cashRegister(request):
    if request.method == 'GET':
        return render(request, 'cashRegister.html', {
            'form': cashRegisterForm()
        })
    else:
        form = cashRegisterForm(request.POST)
        if form.is_valid() :
            CashDonation.objects.create(
                cash = request.POST['cash'],
                date = timezone.now(),
                name = request.POST['name'],
                surname = request.POST['surname'],
                dniDonor = request.POST['dniDonor']
            )
            return redirect('donation')

@login_required
def makeComent(request):
        form = ComentPublicationForm(request.POST)
        if form.is_valid() :
            publication_id = request.POST.get('id')
            logged_user = request.user
            publication = get_object_or_404(Publication, id=publication_id)
            comentText = request.POST['text']

            if len(comentText) > 254 :
                messages.error(request, 'El comentario deber tener menos de 255 caracteres')
                return redirect('post', publication_id)
            Coment.objects.create(
                parent_id = None,
                author = logged_user,
                publication = publication,
                text = request.POST['text']
            )
        return redirect('post', publication_id)

@login_required
def viewComents(request):
    if request.method == 'GET':    
        publication_id = request.GET.get('id')
        publicacion = Publication.objects.get( id=publication_id )
        coments = Coment.objects.filter(publication = publication_id)
        return render(request, 'coments.html',{
            'coments' : coments,
            'publication' : publicacion,
            'form' : ComentPublicationForm()
         })

@login_required
def makeResponse(request, id):

    logged_user = request.user
    coment = get_object_or_404(Coment, id=id)
    publication = coment.publication
    publication_id = publication.id
    coments = Coment.objects.filter(publication = publication_id)

    Coment.objects.create(
        parent_id = coment,
        author = logged_user,
        publication = publication,
        text = request.POST['text']
    )
    return render(request, 'coments.html',{
            'coments' : coments,
            'publication' : publication,
            'form' : ComentPublicationForm()
         })
    
def user_delete_post(request, id):
    if request.method == 'POST': 
        message = None
        myPosts = Publication.objects.filter(user=request.user)
        publicacion = get_object_or_404(Publication, id=id)
        if not Offer.objects.filter(post_id=publicacion.id).exists():
            publicacion.delete()
            message = 'Publicacion eliminada'
        else:
            message = 'La publicacion no puede eliminarse porque tiene ofertas pendientes'

        return render(request, 'my-posts.html', {
            'myPosts' : myPosts,
            'msg': message
        })

def offer_post(request, post_id):
    if request.method == 'GET':
        return render(request, 'make_offer.html', {
            'form': CreateNewOffer()
        })
    else:
        form = CreateNewOffer(request.POST)

        if form.is_valid():
            post = get_object_or_404(Publication, id=post_id)

            # Crear la oferta usando los datos validados del formulario
            Offer.objects.create(
                title=form.cleaned_data['title'],
                date=form.cleaned_data['date'],
                hour=form.cleaned_data['hour'],
                sede=form.cleaned_data['sede'],
                description=form.cleaned_data['description'],
                user=request.user,
                post=post
            )
            message = 'Oferta realizada con éxito'
        else:
            message = None
    
        return render(request, 'make_offer.html',{'form': form,
                                               'message': message})
    

#Ofertas hechas a mi publicacion
def show_my_offers(request, id):
    if request.method == 'GET':
        message = None
        title = Publication.objects.get(id=id).title
        offers = Offer.objects.filter(post__in=Publication.objects.filter(user=request.user))
        if not offers:
            message = 'No hay ofertas para esta publicación'
        return render(request, 'view-my-offers.html',{
            'myOffers' : offers,
            'title' :title,
            'msg' : message
        })

#Ofertas propias realizadas
def show_offers(request):
    if request.method == 'GET':
        message = None
        offers = Offer.objects.filter(user=request.user)

        if not offers:
            message = 'No realizaste ofertas'

        return render(request, 'offers.html',{
            'myOffers' : offers,
            'msg' : message
        })


def decline_offer(request,id):
    if request.method == 'POST':
        message = 'Oferta rechazada'
        offer = get_object_or_404(Offer, id=id)
        offers = Offer.objects.filter(post__in=Publication.objects.filter(user=request.user))
        offer.delete()

        back.enviarMail(offer.user.mail,'Oferta rechazada', f'Hola {offer.user.name}, el usuario {offer.post.user.name} {offer.post.user.surname} a rechazado la oferta {offer.title}')

        return render(request, 'view-my-offers.html',{
            'myOffers' : offers,
            'msg': message
        })
    
def accept_offer(request,id):
    if request.method == 'POST':
        message = None
        offer = get_object_or_404(Offer, id=id)
        offers = Offer.objects.filter(post__in=Publication.objects.filter(user=request.user))
        #offer.delete()
        
        # chequear que esa publicacion no este en un intercambio creado
        post_offer = Publication.objects.get(id = offer.post_id)
        try:
            post_intercambio = Intercambio.objects.get(post=post_offer)
            # Si se encuentra un intercambio, no se puede aceptar otra oferta
            message = 'No puedes aceptar más de una oferta con un intercambio en curso.'
        except Intercambio.DoesNotExist:
            # Crear intercambio
            Intercambio.objects.create(
                date=offer.date,
                offerOwner=offer.user,
                post=post_offer
            )

            post_offer.isHide = True
            post_offer.save()  # Guarda los cambios en la base de datos

            # enviar mail al ofertador de oferta aceptada
            back.enviarMail(offer.user.mail,'Oferta aceptada', f'Hola {offer.user.name}, el usuario {offer.post.user.name} {offer.post.user.surname} a aceptado la oferta {offer.title}')

            message = 'Oferta aceptada con éxito.'

        return render(request, 'view-my-offers.html',{
            'myOffers' : offers,
            'msg': message
        })
    
def cancel_offer(request,id):
    if request.method == 'POST':
        message = 'Oferta cancelada'
        offer = get_object_or_404(Offer, id=id)
        offers = Offer.objects.filter(user=request.user)
        back.enviarMail(offer.post.user.mail,'Oferta cancelada', f'Hola {offer.post.user.name}, el usuario {offer.user.name} {offer.user.surname} a cancelado la oferta {offer.title}')
        offer.delete()

        return render(request, 'offers.html',{
            'myOffers' : offers,
            'msg': message
        })
    
def delete_all_users(request):
    if request.method == 'POST':
        users_to_delete = User.objects.filter(rol__in=['1', '2'])
    
        # Filtra y elimina las instancias relacionadas
        Publication.objects.filter(user__in=users_to_delete).delete()
        Offer.objects.filter(user__in=users_to_delete).delete()
        Intercambio.objects.filter(offerOwner__in=users_to_delete).delete()

        users_to_delete.delete()
        return redirect('view_asignar_colaborador')
    

def article_register(request):
     if request.method == 'GET':
        return render(request, 'articleRegister.html', {
            'form': articleRegisterForm()
        })
     else:
        form = articleRegisterForm(request.POST)
        if form.is_valid() :
            ArticleDonation.objects.create(
                article = request.POST['article'],
                category = request.POST['category'],
                date = timezone.now(),
                name = request.POST['name'],
                surname = request.POST['surname'],
                dniDonor = request.POST['dniDonor']
            )
            message = 'Donación de articulo registrada con exito.'
            return render(request, 'articleRegister.html',{
                'form': articleRegisterForm(),
                'msg': message
            })
        
def show_articles(request):
    if request.method == 'GET':
        articles = ArticleDonation.objects.all()
        if not articles:
            message = 'No se registraron donaciones de articulos.'
        else:
            message = None
        
        return render(request, 'show-articles.html',{
            'articles': articles,
            'msg': message
        })
    
def show_intercambios_today(request):
    if request.method == 'GET':
        today = datetime.now().date()
        intercambios = Intercambio.objects.filter(isDone = False, date = today) # chequear

        if not intercambios :
            message = 'No hay intercambios pendientes en el dia de la fecha.'
        else:
            message = None
        
        return render(request, 'show-intercambios-dia.html', {
            'intercambios': intercambios,
            'msg': message
        })
    
def confirm_intercambio(request, id):
    if request.method == 'POST':
        #agarrar intercambio con el id que llega
        url = 'http://127.0.0.1:8000/calificar-intercambio'
        intercambio = get_object_or_404(Intercambio, id = id)

        #poner isDone = True
        intercambio.isDone = True

        #mandar mails a integrantes con link para calificacion
        user1 = intercambio.post.user
        user2 = intercambio.offerOwner

        #back.send_email('http://127.0.0.1:8000/', user1.mail)
        back.enviarMail(user1.mail, 'Calificar Intercambio', f'Hola {user1.name}, nos gustaría que nos dejes tu reseña con una calificación sobre el intercambio. Califica aqui: {url}/{id}')
        back.enviarMail(user2.mail, 'Calificar Intercambio', f'Hola {user2.name}, nos gustaría que nos dejes tu reseña con una calificación sobre el intercambio. Califica aqui: {url}/{id}')

        return render(request, 'show-intercambios-dia.html')
       # back.enviarMail(user1.mail, 'Calificar Intercambio', f'Hola {user1.name}, nos gustaría que nos dejes tu reseña con una calificación sobre el intercambio. Por favor, califica tu experiencia aquí: <a href="URL_DE_TU_SITIO_PARA_CALIFICAR">Calificar Intercambio</a>')
       # back.enviarMail(user1.mail,'Calificar Intercambio', f'Hola {user1.name} nos gustaria que nos dejes tu reseña con una calificacion sobre el intercambio. Entra aqui: <a href="URL_DE_TU_SITIO_PARA_CALIFICAR">Calificar Intercambio</a> ')
       # back.enviarMail(user2.mail,'Calificar Intercambio', f'Hola {user2.name} nos gustaria que nos dejes tu reseña con una calificacion sobre el intercambio ')
    



def decline_intercambio(request, id):
    if request.method == 'POST':
        intercambio = get_object_or_404(Intercambio, id= id)

        intercambio.post.isHide = False

        Intercambio.objects.delete(id=id)

@login_required
def calificar_intercambio(request, id): # id del intercambio del

    # Tomo el intercambio a ser calificado
    intercambio = Intercambio.objects.get(id=id)
    message = None
    if request.method == "GET":
        return render(request, 'calificar-intercambio.html', {
                'form': calificationForm(),
                'intercambio': intercambio.post.title,
                'msg': message
            })
    else:
        form = calificationForm(request.POST)

        if Calification.objects.filter(user=request.user, intercambio_id=id).exists():
            message = "Ya realizaste una calificación para este intercambio."
            return render(request, 'calificar-intercambio.html', {
                'form': calificationForm(),
                'intercambio': intercambio.post.title,
                'msg': message
            })

        if form.is_valid():
            Calification.objects.create(
                intercambio = intercambio,
                user = request.user,
                calification = request.POST['calification']
            )

        return render(request, 'show-all-posts.html')



def show_my_cards(request):
    if request.method == 'GET':
        logged_user = request.user
        myCards = Card.objects.filter(user = logged_user)

        if not myCards:
            message = 'No hay tarjetas cargadas'
        else:
            message = None
        
    return render(request, 'my-cards.html',{
        'myCards' : myCards,
        'msg': message
    })

def delete_card(request, id):
    if request.method == 'POST': 
        message = None
        card = get_object_or_404(Card, id=id, user=request.user)
        
        card.delete()
        message = 'Tarjeta eliminada con exito.'

        myCards = Card.objects.filter(user=request.user)

        return render(request, 'my-cards.html', {
            'myCards' : myCards,
            'msg': message
        })