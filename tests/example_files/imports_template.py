from rest_framework.serializers import Serializer

x: [str, Serializer]
y: (str, str, ...)


def test(a: [([str], Serializer)], b: str = '') -> [str]:
    pass
