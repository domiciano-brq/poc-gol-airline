from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passageiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('data_nascimento', models.DateField()),
            ],
            options={
                'verbose_name': 'Passageiro',
                'verbose_name_plural': 'Passageiros',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Voo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, unique=True)),
                ('origem', models.CharField(max_length=3)),
                ('destino', models.CharField(max_length=3)),
                ('data_partida', models.DateTimeField()),
                ('data_chegada', models.DateTimeField()),
                ('capacidade', models.PositiveIntegerField()),
                ('status', models.CharField(
                    choices=[
                        ('agendado', 'Agendado'),
                        ('cancelado', 'Cancelado'),
                        ('concluido', 'Concluido'),
                    ],
                    default='agendado',
                    max_length=20,
                )),
            ],
            options={
                'verbose_name': 'Voo',
                'verbose_name_plural': 'Voos',
                'ordering': ['data_partida'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assento', models.CharField(max_length=5)),
                ('status', models.CharField(
                    choices=[
                        ('confirmada', 'Confirmada'),
                        ('cancelada', 'Cancelada'),
                        ('pendente', 'Pendente'),
                    ],
                    default='pendente',
                    max_length=20,
                )),
                ('data_reserva', models.DateTimeField(auto_now_add=True)),
                ('voo', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reservas',
                    to='voos.voo',
                )),
                ('passageiro', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reservas',
                    to='voos.passageiro',
                )),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['-data_reserva'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='reserva',
            unique_together={('voo', 'assento')},
        ),
    ]
