from rest_framework import viewsets
from .models import Voo
from .serializers import VooSerializer


class VooViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Voo.objects.all()
    serializer_class = VooSerializer

    def get_queryset(self):
        queryset = Voo.objects.all()

        origem = self.request.query_params.get('origem')
        destino = self.request.query_params.get('destino')
        data = self.request.query_params.get('data')

        if origem:
            queryset = queryset.filter(origem__iexact=origem)
        if destino:
            queryset = queryset.filter(destino__iexact=destino)
        if data:
            queryset = queryset.filter(data_partida__date=data)

        return queryset
