from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Autor, Livro
from django.contrib.auth.decorators import login_required

# Create your views here.
def livros(request):
    #return HttpResponse('Olá mundo')
    return render(request, 'livros.html')

def salva_livros(request):
    titulo_livro = request.POST['titulo_livro']
    autor_livro = request.POST['autor_livro']
    editora_livro = request.POST['editora_livro']
    return render(request, 'livros.html', context = {'titulo_livro': titulo_livro})
    #return HttpResponse('Livro salvo!' + titulo_livro)

@login_required
def cadastra_livro(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        titulo = request.POST['titulo']
        autor_nome = request.POST['autor']
        ano_publicacao = request.POST['ano_publicacao']
        editora = request.POST['editora']
        
        # Novos campos do livro
        descricao = request.POST.get('descricao', '')
        tem_audiobook = request.POST.get('tem_audiobook') == 'on'
        link_audiobook = request.POST.get('link_audiobook', '')
        plataforma_audiobook = request.POST.get('plataforma_audiobook', '')
        
        # Dados do autor
        biografia = request.POST.get('biografia', '')
        nacionalidade = request.POST.get('nacionalidade', '')
        data_nascimento = request.POST.get('data_nascimento', None)

        # Busca ou cria o autor com os dados adicionais
        autor, created = Autor.objects.get_or_create(
            nome=autor_nome,
            defaults={
                'biografia': biografia,
                'nacionalidade': nacionalidade,
                'data_nascimento': data_nascimento if data_nascimento else None
            }
        )
        
        # Se o autor já existia, atualiza os dados se foram fornecidos
        if not created and (biografia or nacionalidade or data_nascimento):
            if biografia:
                autor.biografia = biografia
            if nacionalidade:
                autor.nacionalidade = nacionalidade
            if data_nascimento:
                autor.data_nascimento = data_nascimento
            autor.save()

        if livro_id:        # Edita livro
            livro = get_object_or_404(Livro, id=livro_id)
            livro.titulo = titulo
            livro.autor = autor
            livro.ano_publicacao = ano_publicacao
            livro.editora = editora
            livro.descricao = descricao
            livro.tem_audiobook = tem_audiobook
            livro.link_audiobook = link_audiobook if tem_audiobook else ''
            livro.plataforma_audiobook = plataforma_audiobook if tem_audiobook else ''
            livro.save()
        else:       # Salva um novo livro
            Livro.objects.create(
                titulo=titulo,
                autor=autor,
                ano_publicacao=ano_publicacao,
                editora=editora,
                descricao=descricao,
                tem_audiobook=tem_audiobook,
                link_audiobook=link_audiobook if tem_audiobook else '',
                plataforma_audiobook=plataforma_audiobook if tem_audiobook else ''
            )
        return redirect('cadastra_livro')
    
    livros = Livro.objects.all()
    autores = Autor.objects.all()
    return render(request, 'livros.html', {'livros': livros, 'autores': autores})

@login_required
def exclui_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    livro.delete()
    return redirect('cadastra_livro')

@login_required
def edita_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    livros = Livro.objects.all()
    autores = Autor.objects.all()

    if request.method == "POST":
        livro.titulo = request.POST['titulo']
        autor_nome = request.POST['autor']
        livro.ano_publicacao = request.POST['ano_publicacao']
        livro.editora = request.POST['editora']
        
        # Novos campos do livro
        livro.descricao = request.POST.get('descricao', '')
        livro.tem_audiobook = request.POST.get('tem_audiobook') == 'on'
        livro.link_audiobook = request.POST.get('link_audiobook', '') if livro.tem_audiobook else ''
        livro.plataforma_audiobook = request.POST.get('plataforma_audiobook', '') if livro.tem_audiobook else ''
        
        # Dados do autor
        biografia = request.POST.get('biografia', '')
        nacionalidade = request.POST.get('nacionalidade', '')
        data_nascimento = request.POST.get('data_nascimento', None)
        
        # Busca ou cria o autor com os dados adicionais
        autor, created = Autor.objects.get_or_create(
            nome=autor_nome,
            defaults={
                'biografia': biografia,
                'nacionalidade': nacionalidade,
                'data_nascimento': data_nascimento if data_nascimento else None
            }
        )
        
        # Se o autor já existia, atualiza os dados se foram fornecidos
        if not created and (biografia or nacionalidade or data_nascimento):
            if biografia:
                autor.biografia = biografia
            if nacionalidade:
                autor.nacionalidade = nacionalidade
            if data_nascimento:
                autor.data_nascimento = data_nascimento
            autor.save()
        
        livro.autor = autor
        livro.save()
        return redirect('cadastra_livro')

    return render(request, 'livros.html', {'livros': livros, 'livro_editar': livro, 'autores': autores})

# Detalhes do livro
@login_required
def detalhes_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    return render(request, 'detalhes_livro.html', {'livro': livro})