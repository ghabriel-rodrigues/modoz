#-*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
from modulos.educacional.models import Curso, Aula, Exercicio, Questao, Alternativa
from datetime import datetime, timedelta

class Professor(models.Model):
    CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    )
    usuario = models.ForeignKey(User,unique=True)
    email = models.EmailField("Email", blank = False, null = True, help_text = "", unique = True)
    nome = models.CharField("Nome", max_length = 255, blank = True, null = True, help_text = "")
    endereco = models.CharField("Endereco", max_length = 255, blank = True, null = True, help_text = "")
    telefone = models.CharField("Telefone", max_length = 14, blank = True, null = True, help_text = "")
    cpf = models.CharField("CPF", max_length = 15, blank = False, null = True, help_text = "", unique=True)
    nascimento = models.CharField("Data de nascimento", max_length = 10, blank = True, null = True, help_text = "")
    sexo = models.CharField(max_length=30,choices=CHOICES, blank=True)
    status = models.BooleanField("Online", help_text = "O usuario está online?", blank = True)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    class Meta:
        verbose_name = u"Professor"
        verbose_name_plural = u"Professores"

    def __str__(self) :
        return u"%s" % self.email

    def __unicode__(self) :
        return u"%s" % self.email

    def getClass(self) :
        return "Professor"

class Aluno(models.Model):
    CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    )
    usuario = models.ForeignKey(User,unique=True)
    email = models.EmailField("Email", blank = False, null = True, help_text = "", unique = True)
    nome = models.CharField("Nome", max_length = 255, blank = True, null = True, help_text = "")
    endereco = models.CharField("Endereco", max_length = 255, blank = True, null = True, help_text = "")
    telefone = models.CharField("Telefone", max_length = 14, blank = True, null = True, help_text = "")
    cpf = models.CharField("CPF", max_length = 15, blank = False, null = True, help_text = "", unique=True)
    nascimento = models.CharField("Data de nascimento", max_length = 10, blank = True, null = True, help_text = "")
    sexo = models.CharField(max_length=30,choices=CHOICES, blank=True)
    status = models.BooleanField("Online", help_text = "O usuario está online?", blank = True)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    class Meta:
        verbose_name = u"Aluno"
        verbose_name_plural = u"Alunos"

    def __str__(self) :
        return u"%s" % self.email

    def __unicode__(self) :
        return u"%s" % self.email

    def getClass(self) :
        return "Aluno"

class MotivoCancelamento(models.Model):
    aluno = models.ForeignKey(Aluno)
    motivo = models.TextField(blank = True, null = True, help_text = "")
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    @classmethod
    def create(cls, aluno, motivo, dataCadastro ):
        motivo = cls( aluno=aluno, motivo=motivo, dataCadastro=dataCadastro)
        # do something with the book
        return motivo

    class Meta:
        verbose_name = u"Motivo de cancelamento"
        verbose_name_plural = u"Motivos"

    def __str__(self) :
        return "%s - %s - %s" % (self.id, self.aluno.nome, self.dataCadastro)

    def __unicode__(self) :
        return "%s - %s - %s" % (self.id, self.aluno.nome, self.dataCadastro)

    def getClass(self) :
        return "Motivo"

class Duvida(models.Model):
    CHOICES = (
        ('respondido', 'Respondido'),
        ('aguardando', 'Aguardando resposta'),
    )
    status = models.CharField(max_length=30,choices=CHOICES, blank=True)
    pergunta = models.TextField(blank = True, null = True, help_text = "")
    resposta = models.TextField(blank = True, null = True, help_text = "")
    aula = models.ForeignKey(Aula,blank=True, null=True)
    aluno = models.ForeignKey(Aluno,blank=True, null=True)
    professor=models.ForeignKey(Professor,blank=True, null=True)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    @classmethod
    def create(cls, status, pergunta, resposta, aula, aluno, professor,dataCadastro ):
        duvida = cls( status=status, pergunta=pergunta, resposta=resposta,
         aula=aula, aluno=aluno, professor=professor,dataCadastro=dataCadastro)
        # do something with the book
        return duvida

    class Meta:
        verbose_name = u"Duvida"
        verbose_name_plural = u"Duvidas"

    def __str__(self) :
        return "%s - %s" % (self.id, self.aluno.nome)

    def __unicode__(self) :
        return "%s - %s" % (self.id, self.aluno.nome)

    def getClass(self) :
        return "Duvida"

class DesempenhoDoAlunoPorExercicio(models.Model):
    aluno = models.ForeignKey(Aluno)
    exercicio = models.ForeignKey(Exercicio)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    respostas = models.ManyToManyField(Alternativa, related_name="porExercicio_porAlternativa",blank = True,null = True)

    questoesAcertadas = models.ManyToManyField(Questao, related_name="porExercicio_porQuestao",blank = True,null = True)
    nota = models.FloatField(blank=False, null=False)
    STATUS = (
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
        ('Andamento', 'Andamento'))
    status = models.CharField(max_length=30,choices=STATUS, blank=True)

    @classmethod
    def create(cls, aluno, exercicio, dataCadastro, status, nota ):
        desempenho = cls(aluno=aluno, exercicio=exercicio, dataCadastro=dataCadastro, status=status, nota=nota)
        return desempenho

    class Meta:
        verbose_name = u"Desempenho do aluno por exercicio"
        verbose_name_plural = u"Desempenhos dos alunos por exercicio"

    def __str__(self) :
        return "%s - %s" % (self.aluno.nome, self.exercicio.titulo)

    def __unicode__(self) :
        return "%s - %s" % (self.aluno.nome, self.exercicio.titulo)

    def getClass(self) :
        return "DesempenhoDoAlunoPorExercicio"

    def get_token_safe(self):
        token = str(self.dataCadastro.second) + str(self.exercicio.aula_exercicio.id) + str(self.id) + str(self.dataCadastro.minute) + self.titulourl
        token_cifrado = base64.b64encode(token)
        return "%s" % (str(token_cifrado))[:15]

class DesempenhoDoAlunoPorAula(models.Model):
    aluno = models.ForeignKey(Aluno)
    aula = models.ForeignKey(Aula)
    desempenhoDosExercicios = models.ManyToManyField(DesempenhoDoAlunoPorExercicio, related_name="porAula_porExercicio",blank = True,null = True)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    STATUS = (
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
        ('Andamento', 'Andamento'))
    status = models.CharField(max_length=30,choices=STATUS, blank=True)

    class Meta:
        verbose_name = u"Desempenho do aluno por aula"
        verbose_name_plural = u"Desempenhos dos alunos por aula"

    def __str__(self) :
        return "%s - %s" % (self.aluno.nome, self.aula.titulo)

    def __unicode__(self) :
        return "%s - %s" % (self.aluno.nome, self.aula.titulo)

    def getClass(self) :
        return "DesempenhoAlunoPorAula"

class DesempenhoDoAlunoPorCurso(models.Model):
    aluno = models.ForeignKey(Aluno)
    curso = models.ForeignKey(Curso)
    desempenhoDasAulas = models.ManyToManyField(DesempenhoDoAlunoPorAula, related_name="porCurso_porAula",blank = True,null = True)
    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    STATUS = (
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
        ('Andamento', 'Andamento'))
    status = models.CharField(max_length=30,choices=STATUS, blank=True)

    class Meta:
        verbose_name = u"Desempenho do aluno por curso"
        verbose_name_plural = u"Desempenhos dos alunos por curso"

    def __str__(self) :
        return "%s - %s" % (self.aluno.nome, self.curso.titulo)

    def __unicode__(self) :
        return "%s - %s" % (self.aluno.nome, self.curso.titulo)

    def getClass(self) :
        return "DesempenhoAlunoPorAula"

class Matricula(models.Model):
    CHOICES = (
        ('Habilitada', 'Habilitada'),
        ('Bloqueada', 'Bloqueada'),
        ('Cancelada', 'Cancelada'),
        ('Finalizada', 'Finalizada'),
    )
    FORMAS = (
        ('credito', 'credito'),
        ('debito', 'debito'),
        ('boleto', 'boleto'),
        ('vista', 'vista'),
    )
    CURSOSTATUS = (
        ('Iniciado', 'Iniciado'),
        ('Andamento', 'Andamento'),
        ('Finalizado', 'Finalizado'),
    )
    numero = models.CharField("Numero", max_length = 255, blank = True, null = True, help_text = "")
    aluno = models.ForeignKey(Aluno,blank=True, null=True)
    curso = models.ForeignKey(Curso,blank=True, null=True)
    cursosituacao = models.CharField("Status curso", max_length=30,choices=CURSOSTATUS, blank=True)
    status = models.CharField(max_length=30,choices=CHOICES, blank=True)
    formasDePagamento = models.CharField(max_length=30,choices=FORMAS, blank=True)
    totalParcelas = models.PositiveIntegerField(verbose_name='Parcelas', blank=True, null=True)
    inicioDoPeriodo = models.DateTimeField(blank = True, null = True)
    terminoDoPeriodo = models.DateTimeField(blank = True, null = True)

    aulasAssistidas = models.ManyToManyField(Aula, related_name="matricula_aulas", verbose_name = "Aulas assistidas", blank = True, null = True)
    exerciciosConcluidos = models.ManyToManyField(Exercicio, related_name="matricula_exercicios", verbose_name = "Exercicios concluidos", blank = True, null = True)

    dataCadastro = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    def __str__(self) :
        return "%s - %s" % (self.aluno.nome, self.curso.titulo)

    def __unicode__(self) :
        return "%s - %s" % (self.aluno.nome, self.curso.titulo)

    def getClass(self) :
        return "DesempenhoAlunoPorAula"

#TODO - TRABALHAR MAIS AQUI
class Visita(models.Model):
    aluno = models.ForeignKey(Aluno,blank=True, null=True)
    horario = models.DateTimeField(auto_now_add = True, blank = True, null = True)
#TODO
#class Performance
