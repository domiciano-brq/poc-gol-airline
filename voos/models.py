from django.db import models


class Voo(models.Model):
    STATUS_AGENDADO = 'agendado'
    STATUS_CANCELADO = 'cancelado'
    STATUS_CONCLUIDO = 'concluido'

    STATUS_CHOICES = [
        (STATUS_AGENDADO, 'Agendado'),
        (STATUS_CANCELADO, 'Cancelado'),
        (STATUS_CONCLUIDO, 'Concluido'),
    ]

    numero = models.CharField(max_length=10, unique=True)
    origem = models.CharField(max_length=3)
    destino = models.CharField(max_length=3)
    data_partida = models.DateTimeField()
    data_chegada = models.DateTimeField()
    capacidade = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AGENDADO)

    class Meta:
        verbose_name = 'Voo'
        verbose_name_plural = 'Voos'
        ordering = ['data_partida']

    def __str__(self):
        return f'{self.numero} ({self.origem} -> {self.destino})'


class Passageiro(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField()

    class Meta:
        verbose_name = 'Passageiro'
        verbose_name_plural = 'Passageiros'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.cpf})'


class Reserva(models.Model):
    STATUS_CONFIRMADA = 'confirmada'
    STATUS_CANCELADA = 'cancelada'
    STATUS_PENDENTE = 'pendente'

    STATUS_CHOICES = [
        (STATUS_CONFIRMADA, 'Confirmada'),
        (STATUS_CANCELADA, 'Cancelada'),
        (STATUS_PENDENTE, 'Pendente'),
    ]

    voo = models.ForeignKey(Voo, on_delete=models.CASCADE, related_name='reservas')
    passageiro = models.ForeignKey(Passageiro, on_delete=models.CASCADE, related_name='reservas')
    assento = models.CharField(max_length=5)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
    data_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        unique_together = ('voo', 'assento')
        ordering = ['-data_reserva']

    def __str__(self):
        return f'Reserva {self.assento} - {self.voo} - {self.passageiro}'
