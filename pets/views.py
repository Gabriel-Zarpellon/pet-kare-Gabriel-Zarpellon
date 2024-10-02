from rest_framework.views import APIView, status, Response, Request
from pets.serializers import PetSerializer
from pets.models import Pet
from traits.models import Trait
from groups.models import Group
from pet_kare.pagination import CustomPageNumberPagination
from django.forms.models import model_to_dict


class PetView(APIView, CustomPageNumberPagination):
    def post(self, request: Request) -> Response:
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

    def get(self, request: Request) -> Response:
        trait_param = request.query_params.get("trait", None)

        if trait_param:
            pets = Pet.objects.filter(traits__name=trait_param).all()
        else:
            pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetDetailedView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.pop("group", None)
        traits = serializer.validated_data.pop("traits", None)

        if traits:
            trait_list = []

            for trait_dict in traits:
                trait = Trait.objects.filter(name__iexact=trait_dict["name"]).first()

                if not trait:
                    trait = Trait.objects.create(**trait_dict)

                trait_list.append(trait)

            pet.traits.set(trait_list)
            pet.save()

        if group:
            group_obj = Group.objects.filter(
                scientific_name__iexact=group["scientific_name"]
            ).first()

            if not group_obj:
                group_obj = Group.objects.create(**group)

            pet.group = group_obj
            pet.save()

        [setattr(pet, key, value) for key, value in serializer.validated_data.items()]

        pet.save()

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)
