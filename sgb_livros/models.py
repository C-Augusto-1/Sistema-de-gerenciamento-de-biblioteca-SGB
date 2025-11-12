from django.db import models

# Create your models here
class Autor(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    nacionalidade = models.CharField(max_length=100, verbose_name='Nacionalidade', blank=True, null=True)
    biografia = models.TextField(verbose_name='Biografia', blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_total_livros(self):
        """Retorna o total de livros do autor"""
        return self.livros.count()  # Usa o related_name 'livros' definido no ForeignKey


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', related_name='livros', on_delete=models.CASCADE)
    ano_publicacao = models.PositiveIntegerField()
    editora = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    
    # Campos de audiobook
    tem_audiobook = models.BooleanField(default=False, verbose_name='Tem Audiobook?')
    link_audiobook = models.URLField(blank=True, null=True, verbose_name='Link do Audiobook')
    plataforma_audiobook = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='Plataforma',
        choices=[
            ('audible', 'Audible'),
            ('spotify', 'Spotify'),
            ('ubook', 'Ubook'),
            ('storytel', 'Storytel'),
            ('youtube', 'YouTube'),
            ('outros', 'Outros')
        ]
    )
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo']

    def __str__(self):
        return f"{self.titulo} - {self.autor.nome}"