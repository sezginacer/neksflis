class MultiSerializerViewSetMixin:
    def get_serializer_class(self):
        try:
            return self.serializers[self.action]
        except (AttributeError, KeyError):
            return super().get_serializer_class()
