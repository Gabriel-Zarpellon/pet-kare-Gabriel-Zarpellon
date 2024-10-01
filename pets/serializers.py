from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):

    SEX_CHOICES = [("Male"), ("Female"), ("Not Informed")]

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SEX_CHOICES, default="Not Informed")

    group = GroupSerializer()
    traits = TraitSerializer(many=True)
