from rest_framework import serializers



class TimetableSerializer(serializers.Serializer):
    tag = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    longname = serializers.CharField(max_length=200, required=False, allow_blank=True)
    dozent = serializers.CharField(max_length=100)
    raum = serializers.CharField(max_length=50)
    startBlock = serializers.IntegerField()
    endBlock = serializers.IntegerField()
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)