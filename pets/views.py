from rest_framework.views import APIView, status
from pets.serializers import PetSerializer
from pets.models import Pet
from traits.models import Trait
from groups.models import Group
from rest_framework.response import Response
from pet_kare.pagination import CustomPageNumberPagination


class PetView(APIView, CustomPageNumberPagination):
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.pop("group")
        traits = serializer.validated_data.pop("traits")

        pet = Pet.objects.create(**serializer.validated_data)

        for trait_dict in traits:
            trait = Trait.objects.filter(name__iexact=trait_dict["name"]).first()

            if not trait:
                trait = Trait.objects.create(**trait_dict)

            pet.traits.add(trait)

        group_obj = Group.objects.filter(
            scientific_name__iexact=group["scientific_name"]
        ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group)

        pet.group = group_obj

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
