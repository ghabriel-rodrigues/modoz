#-*- coding: utf-8 -*-
from django.db import models
import base64

#Importa a biblioteca grafica do Python (PIL - Python Imaging Library)
try:
    import Image
except ImportError:
    try:
        pass
        #from modoz.modulos.PIL import Image
    except ImportError:
        raise ImportError(u"Projeto modoz n\u00E3o conseguiu importar a biblioteca de imagem do Python (Python Imaging Library).")


class Tema(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField("Tema", max_length = 255, blank = True, null = True, help_text = "")
    descricao = models.TextField(blank = True, null = True, help_text = "")
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    titulourl = models.SlugField(verbose_name="URL amigavel para o tema",unique = True, blank = False, null = True, help_text = u"URLs devem ser compostos apenas de letras minusculas, '_' , '-' e numeros.")


    class Meta:
        verbose_name = u"Tema"
        verbose_name_plural = u"0. Temas"

    def __str__(self) :
        return "%s - %s" % (self.id, self.titulo)

    def __unicode__(self) :
        return "%s - %s" % (self.id, self.titulo)

    def getClass(self) :
        return "Tema"

    def getURL(self) :
        return "%s" % self.titulourl


class Alternativa(models.Model):
    id = models.AutoField(primary_key=True)
    enunciadoAbreviado = models.CharField("Enunciado abreviado", max_length = 255, blank = True, null = True, help_text = "")
    tema = models.ForeignKey(Tema,blank=True, null=True)
    enunciado = models.TextField(blank = True, null = True, help_text = "")
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    class Meta:
        verbose_name = u"Alternativa"
        verbose_name_plural = u"1. Alternativas"

    def __str__(self) :
        return "%s" % (self.enunciadoAbreviado)

    def __unicode__(self) :
        return "%s" % (self.enunciadoAbreviado)

    def getClass(self) :
        return "Alternativa"


class Questao(models.Model):
    id = models.AutoField(primary_key=True)
    tema = models.ForeignKey(Tema,blank=True, null=True)
    perguntaAbreviada = models.CharField("Pergunta abreviada", max_length = 255, blank = True, null = True, help_text = "")
    pergunta = models.TextField("Pergunta", blank = True, null = True, help_text = "")
    respostaCorreta = models.ForeignKey(Alternativa, blank=False, null=False)
    alternativas = models.ManyToManyField(Alternativa, related_name="questao_alternativa", verbose_name = "Alternativas", blank = True, null = True)
    imagem = models.ImageField(u"Imagem", upload_to = "img/questoes", blank = True, null = True)

    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    class Meta:
        verbose_name = u"Questao"
        verbose_name_plural = u"2. Questoes"

    def criar_miniaturas(self):
        if self.imagem:
            self.criar_miniatura_admin()
            self.criar_miniatura_padrao()

    def criar_miniatura_admin(self):
        foto = Image.open(self.imagem.path)
        thumbnail_path = "%s/img/questoes/thumbnails/admin_%s" % (settings.MEDIA_ROOT, self.imagem.name[13:])
        dimensoes = (200, 88)
        foto.thumbnail(dimensoes, Image.ANTIALIAS)
        foto.save(thumbnail_path, foto.format)

    def criar_miniatura_padrao(self):
        foto = Image.open(self.imagem.path)
        thumbnail_path = "%s/img/questoes/thumbnails/padrao_%s" % (settings.MEDIA_ROOT, self.imagem.name[13:])
        dimensoes = (939, 256)
        foto.thumbnail(dimensoes, Image.ANTIALIAS)
        foto.save(thumbnail_path, foto.format)

    def admin_thumbnail(self) :
        return u'<a href="%simg/questoes/%s" class="fancy-trigger"><img src="%simg/ofertas/thumbnails/admin_%s"/></a>' % (settings.MEDIA_URL, self.imagem.name[13:], settings.MEDIA_URL, self.imagem.name[13:])
    admin_thumbnail.short_description = 'Imagem'
    admin_thumbnail.allow_tags = True

    def deletar_miniaturas(self):
        try:
            thumbnail_dir = "%s/img/questoes/thumbnails/" % settings.MEDIA_ROOT
            thumbnail_file = "admin_%s" % self.imagem.name[13:]
            os.unlink("%s%s" % (thumbnail_dir, thumbnail_file))
            thumbnail_file = "padrao_%s" % self.imagem.name[13:]
            os.unlink("%s%s" % (thumbnail_dir, thumbnail_file))
        except Exception:
            pass

    def __str__(self) :
        return "%s - %s" % (self.id, self.perguntaAbreviada)

    def __unicode__(self) :
        return "%s - %s" % (self.id, self.perguntaAbreviada)

    def getClass(self) :
        return "Questao"

class Aula(models.Model):
    tema = models.ForeignKey(Tema, blank=True, null=True)
    titulo = models.CharField("Titulo", max_length = 255, blank = True, null = True, help_text = "")
    titulourl = models.SlugField(verbose_name="URL amigavel para a aula",unique = True, blank = False, null = True, help_text = u"URLs devem ser compostos apenas de letras minusculas, '_' , '-' e numeros.")
    descricao = models.TextField("Descricao", blank = True, null = True, help_text = "")
    urlYoutube = models.CharField(u"Url do video", max_length=150, blank=True, null=True,help_text = u"Insira a URL do video da aula.")
    anexos = models.FileField(upload_to='aulas', blank = True, null = True)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    relates_to = models.ForeignKey('self', verbose_name="Proxima aula", blank = True, null = True)

    class Meta:
        verbose_name = u"Aula"
        verbose_name_plural = u"4. Aulas"

    def __str__(self) :
        return "%s" % (self.titulo)

    def __unicode__(self) :
        return "%s" % (self.titulo)

    def getClass(self) :
        return "Aula"

    def getURL(self) :
        return "%s" % self.titulourl

    def getVideoID(self):
        return "%s" % self.urlYoutube[30:41]

class Exercicio(models.Model):
    CHOICES = (
        ('normal', 'normal'),
        ('avaliacao','avaliacao'),
    )
    status = models.CharField(max_length=30,choices=CHOICES, blank=True)
    tema = models.ForeignKey(Tema,blank=True, null=True)
    aula = models.ForeignKey(Aula,blank=True, null=True)
    titulo = models.CharField("Titulo", max_length = 255, blank = True, null = True, help_text = "")
    titulourl = models.SlugField(verbose_name="URL amigavel para o exercicio",unique = True, blank = False, null = True, help_text = u"URLs devem ser compostos apenas de letras minusculas, '_' , '-' e numeros.")

    descricao = models.TextField("Descricao", blank = True, null = True, help_text = "")
    questoes = models.ManyToManyField(Questao, related_name="exercicio_questao", verbose_name = "Questões", blank = True, null = True)
    aprovarCom75 = models.BooleanField("Aprovar com 75%", blank = True)
    totalQuestoes = models.PositiveIntegerField(verbose_name='Criterio de Aprovação',help_text="Quantidade total de questões corretas necessárias para aprovação:", blank=True, null=True)

    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    class Meta:
        verbose_name = u"Exercicio"
        verbose_name_plural = u"3. Exercicios"

    def __str__(self) :
        return "%s - %s" % (self.tema, self.titulo)

    def __unicode__(self) :
        return "%s - %s" % (self.tema, self.titulo)

    def getClass(self) :
        return "Exercicio"

    def getURL(self) :
        return "%s" % self.titulourl

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    tema = models.ForeignKey(Tema, blank=True, null=True)
    aulaInaugural = models.ForeignKey(Aula, blank=True, null=True)
    titulo = models.CharField("Titulo", max_length = 255, blank = True, null = True, help_text = "")
    titulourl = models.SlugField(verbose_name="URL amigavel para o curso",unique = True, blank = False, null = True, help_text = u"URLs devem ser compostos apenas de letras minusculas, '_' , '-' e numeros.")
    urlYoutube = models.CharField(u"Url do video", max_length=150, blank=True, null=True,help_text = u"Insira a URL do video para apresentar o curso.")
    descricao = models.TextField("Descricao", blank = True, null = True, help_text = "")
    anexos = models.FileField(upload_to='cursos', blank = True, null = True)
    aulas = models.ManyToManyField(Aula, related_name="curso_aula", verbose_name = "Aulas", blank = True, null = True)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    diasDisponiveis = models.PositiveIntegerField(verbose_name='Numero de dias de curso',
        help_text="Número de dias disponibilizados para o aluno utilizar o curso até expirar.", blank=True, null=True)


    class Meta:
        verbose_name = u"Curso"
        verbose_name_plural = u"5. Cursos"

    def __str__(self) :
        return "%s" % (self.titulo)

    def __unicode__(self) :
        return "%s" % (self.titulo)

    def getClass(self) :
        return "Curso"

    def getURL(self) :
        return "%s" % self.titulourl

    def getVideoID(self):
        return "%s" % self.urlYoutube[30:41]
