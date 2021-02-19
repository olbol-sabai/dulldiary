from rest_framework import generics, permissions, pagination, response
from entries.models import Entry
from .serializers import EntryDetailSerializer, EntryListSerializer
from .permissions import OnlyOwnerCanUpdateDelete



class EntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        OnlyOwnerCanUpdateDelete
        ]
    queryset = Entry.objects.all()
    lookup_field = 'id'
    serializer_class = EntryDetailSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print('over here')
        return self.destroy(request, *args, **kwargs)
    
    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}


class ThreePagePagination(pagination.PageNumberPagination):
    page_size = 3
    
    

class EntryListAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ThreePagePagination
    queryset = Entry.objects.all()
    serializer_class = EntryListSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get_serializer_context(self):
        return {"request": self.request}
    
    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    
