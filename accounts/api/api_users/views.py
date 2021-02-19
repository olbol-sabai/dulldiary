from rest_framework import generics, mixins, permissions, parsers, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
UserModel = get_user_model()
from entries.models import Entry

from .permissions import MustBeUserOrSafeMethod
from .serializers import UserSerializer

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['image']


class UploadProfileImageAPIView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [MustBeUserOrSafeMethod]

    def patch(self, request, *args, **kwargs):
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = kwargs.get("username", None)
            user = UserModel.objects.get(username__iexact=username)
            image = serializer.validated_data.get("image")
            user.image = image
            user.save()
            return Response({"detail": 'yo'}, status=204)
        else: 
            return Response({'detail': 'Not going to happen'})



class UserDetailAPIView(
    mixins.UpdateModelMixin, 
    generics.RetrieveAPIView):
    permission_classes = [MustBeUserOrSafeMethod]
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        if username == None:
            return UserModel.objects.none()
        return UserModel.objects.filter(username=username)
    
    def patch(self, request, *args, **kwargs):
        appr_entry_id = request.data.pop('appreciated_entries', None)
        changed_perc_id = request.data.pop('changed_perception', None)
        if isinstance(request.user, UserModel):
            if appr_entry_id is not None:
                entry = Entry.objects.get(id=int(appr_entry_id))
                if entry in request.user.appreciated_entries.all():
                    request.user.appreciated_entries.remove(entry)
                else:
                    request.user.appreciated_entries.add(entry)  
                request.user.save()         
                return Response(status=status.HTTP_200_OK)

            if changed_perc_id is not None:
                entry = Entry.objects.get(id=int(changed_perc_id))
                if entry in request.user.changed_perception_entries.all():
                    request.user.changed_perception_entries.remove(entry)
                else:
                    request.user.changed_perception_entries.add(entry)
                request.user.save()
                return Response(status=status.HTTP_200_OK)
        return self.update(request, *args, *kwargs)

    def get_serializer_context(self):
        return {"request": self.request}

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    lookup_field = 'id'
    queryset = UserModel.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}

        