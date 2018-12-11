#-*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Aluno, Duvida, Matricula
from django.contrib.auth.models import User
from django import forms
from modoz.modulos.educacional.models import Curso, Aula
from modoz.modulos.utils.cpf import CPF

class FormAlterarDados(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','email','password','last_name')
        exclude = ('email','username','first_name','last_name')

    CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino','Feminino'),
    )

    nome = forms.CharField(max_length = 255,required=False)
    endereco = forms.CharField(max_length = 255, required=False)
    telefone = forms.CharField(max_length = 14, required=False)
    cpf = forms.CharField(max_length = 15,required=False)
    email = forms.EmailField(required=False)
    nascimento = forms.DateField(required=False)
    sexo = forms.ChoiceField(choices=CHOICES,required=False)
    status = forms.BooleanField(required=False)
    data = forms.DateTimeField(input_formats='%d-%m-%Y %H:%M:%S',required=False)
    confirme = forms.CharField(max_length=30, widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        self.base_fields['password'].widget = forms.PasswordInput()
        super(FormAlterarDados, self).__init__(*args, **kwargs)


    def clean_confirme(self):
        if self.cleaned_data['confirme'] != self.data['password']:
            raise forms.ValidationError('Confirmacao da senha nao confere, por favor verifique se a senha e o confirme estao iguais')
        return self.cleaned_data['confirme']

    def save(self, commit=True):
        usuario = super(FormAlterarDados, self).save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.username = self.cleaned_data['email']

        if commit:
            usuario.save()

        return usuario

class FormCancelarMatricula(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','email','password','last_name')
        exclude = ('email','username','first_name','last_name')

    nome = forms.CharField(max_length = 255,required=False)
    email = forms.EmailField(required=False)
    telefone = forms.CharField(max_length = 14, required=False)
    confirme = forms.CharField(max_length=30, widget=forms.PasswordInput)
    motivo = forms.CharField(max_length=5000, widget=forms.Textarea, required=True)


    def __init__(self, *args, **kwargs):
        self.base_fields['password'].widget = forms.PasswordInput()
        super(FormCancelarMatricula, self).__init__(*args, **kwargs)

    def clean_confirme(self):
        if self.cleaned_data['confirme'] != self.data['password']:
            raise forms.ValidationError('Confirmacao da senha nao confere, por favor verifique se a senha e o confirme estao iguais')
        return self.cleaned_data['confirme']

    def save(self, commit=True):
        usuario = super(FormCancelarMatricula, self).save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.username = self.cleaned_data['email']

        if commit:
            usuario.save()

        return usuario

class FormDuvidas(ModelForm):
    class Meta:
        model = Duvida


    def __init__(self, user, *args, **kwargs):
        super(FormDuvidas, self).__init__(*args, **kwargs)
        aulaPorCursos = None
        cursos = Matricula.objects.values_list('curso').filter(aluno__email__exact=user.email)

        for curso in cursos:
            if aulaPorCursos == None:
                aulaPorCursos = Aula.objects.filter(curso_aula=curso)
            else:
                aulaPorCursos |= Aula.objects.filter(curso_aula=curso)

        self.fields['aula'].queryset = aulaPorCursos
        pergunta = forms.CharField(max_length=10000, widget=forms.Textarea, required=True)

    def clean_aula(self):
        aulaID = self.cleaned_data['aula']
        if aulaID == "" or aulaID == None or aulaID =='':
            raise forms.ValidationError('Por favor informe a aula')
        return self.cleaned_data['aula']

    def clean_pergunta(self):
        pergunta = self.cleaned_data['pergunta']
        if pergunta == "" or pergunta == None or pergunta =='':
            raise forms.ValidationError('Por favor informe a pergunta')
        return self.cleaned_data['pergunta']

    # def save(self, commit=True):
    #     duvida = super(FormDuvidas, self).save(commit=False)
    #     return duvida


class FormAluno(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','email','password','last_name')
        exclude = ('username')

    CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino','Feminino'),
    )

    nome = forms.CharField(max_length = 255,required=False)
    email = forms.EmailField()
    endereco = forms.CharField(max_length = 255,required=False)
    telefone = forms.CharField(max_length = 14,required=False)
    cpf = forms.CharField(max_length = 15,required=False)
    nascimento = forms.DateField(required=False)
    sexo = forms.ChoiceField(choices=CHOICES,required=False)
    status = forms.BooleanField(required=False)
    data = forms.DateTimeField(input_formats='%d-%m-%Y %H:%M:%S',required=False)
    confirme = forms.CharField(max_length=30, widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        #self.base_fields['password'].help_text = 'Informe uma senha segura'
        self.base_fields['password'].widget = forms.PasswordInput()
        super(FormAluno, self).__init__(*args, **kwargs)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username'],).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este LOGIN')
        return self.cleaned_data['username']

    # def clean_telefone(self):
    #     num = self.cleaned_data['telefone'][5:6]
    #     if num != "6" and num != "7" and num != "8" and num != "9":
    #         raise forms.ValidationError('Por favor insira um numero de celular valido')
    #         #raise forms.ValidationError(self.cleaned_data['telefone'][5:6])
    #     return self.cleaned_data['telefone']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email'],).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este EMAIL')
        return self.cleaned_data['email']

    def clean_cpf(self):
        if Aluno.objects.filter(cpf=self.cleaned_data['cpf'],).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este CPF')
        else:
            try:
                cpf = CPF(self.cleaned_data['cpf'])
                if cpf.valido():
                    return self.cleaned_data['cpf']
                else:
                    raise forms.ValidationError('Por favor informe um CPF valido')
            except:
                raise forms.ValidationError('Por favor informe um CPF valido')
        return self.cleaned_data['cpf']

    def clean_confirme(self):
        if self.cleaned_data['confirme'] != self.data['password']:
            raise forms.ValidationError('Confirmacao da senha nao confere, por favor verifique se a senha e o confirme estao iguais')
        return self.cleaned_data['confirme']

    def save(self, commit=True):
        usuario = super(FormAluno, self).save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.username = self.cleaned_data['email']

        if commit:
            usuario.save()

        return usuario

class FormProfessor(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','email','password','last_name')
        exclude = ('username')

    CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino','Feminino'),
    )

    nome = forms.CharField(max_length = 255,required=False)
    email = forms.EmailField()
    endereco = forms.CharField(max_length = 255,required=False)
    telefone = forms.CharField(max_length = 14,required=False)
    cpf = forms.CharField(max_length = 15,required=False)
    nascimento = forms.DateField(required=False)
    sexo = forms.ChoiceField(choices=CHOICES,required=False)
    status = forms.BooleanField(required=False)
    data = forms.DateTimeField(input_formats='%d-%m-%Y %H:%M:%S',required=False)
    confirme = forms.CharField(max_length=30, widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        #self.base_fields['password'].help_text = 'Informe uma senha segura'
        self.base_fields['password'].widget = forms.PasswordInput()
        super(FormAluno, self).__init__(*args, **kwargs)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username'],).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este LOGIN')
        return self.cleaned_data['username']

    def clean_telefone(self):
        num = self.cleaned_data['telefone'][5:6]
        if num != "6" and num != "7" and num != "8" and num != "9":
            raise forms.ValidationError('Por favor insira um numero de celular valido')
            #raise forms.ValidationError(self.cleaned_data['telefone'][5:6])
        return self.cleaned_data['telefone']

    #def clean_nascimento(self):
    #    if int(self.cleaned_data['nascimento'].day) <= 0 or int(self.cleaned_data['nascimento'].day) > 31 :
    #        raise forms.ValidationError('Informe uma data de nascimento valida - Erro no dia informado')
    #
    #    if int(self.cleaned_data['nascimento'].month) <= 0 or int(self.cleaned_data['nascimento'].month) > 12 :
    #        raise forms.ValidationError('Informe uma data de nascimento valida - Erro no mes informado')
    #
    #    if int(self.cleaned_data['nascimento'].year) <= 1900 or int(self.cleaned_data['nascimento'].year) >= 1992  :
    #        raise forms.ValidationError('Informe uma data de nascimento valida - Erro no ano informado')
    #
    #    return self.cleaned_data['nascimento']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email'],).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este EMAIL')
        return self.cleaned_data['email']

    #def clean_rg(self):
    #    if Aluno.objects.filter(rg=self.cleaned_data['rg'],).count():
    #        raise forms.ValidationError('Ja existe um usuario cadastrado com este RG')
    #    return self.cleaned_data['rg']

    def clean_cpf(self):
        if Aluno.objects.filter(cpf=self.cleaned_data['cpf'],).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este CPF')
        else:
            try:
                cpf = CPF(self.cleaned_data['cpf'])
                if cpf.valido():
                    return self.cleaned_data['cpf']
                else:
                    raise forms.ValidationError('Por favor informe um CPF valido')
            except:
                raise forms.ValidationError('Por favor informe um CPF valido')
        return self.cleaned_data['cpf']

    def clean_confirme(self):
        if self.cleaned_data['confirme'] != self.data['password']:
            raise forms.ValidationError('Confirmacao da senha nao confere, por favor verifique se a senha e o confirme estao iguais')
        return self.cleaned_data['confirme']

    def save(self, commit=True):
        usuario = super(FormProfessor, self).save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.username = self.cleaned_data['email']

        if commit:
            usuario.save()

        return usuario
