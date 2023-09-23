from typing import Any, final

from django import forms

from server.apps.pictures.models import FavouritePicture


@final
class FavouritesForm(forms.ModelForm[FavouritePicture]):
    """Model form for :class:`FavouritePicture`."""

    class Meta(object):
        model = FavouritePicture
        fields = ('foreign_id', 'url')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """We need an extra context: which user is adding items."""
        self._user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> FavouritePicture:
        """Add user to the model instance."""
        instance = super().save(commit=False)
        instance.user_id = self._user.id
        if commit:
            instance.save()
        return instance


@final
class DeleteFavouritesForm(forms.ModelForm[FavouritePicture]):
    """Model form for :class:`FavouritePicture`."""

    class Meta(object):
        model = FavouritePicture
        fields = ('id',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """We need an extra context: which user is deleted items."""
        self._user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def delete(self) -> None:
        """Delete the model instance."""
        try:
            FavouritePicture.objects.get(id=self.data.get('id'), user_id=self._user.id).delete()
        except FavouritePicture.DoesNotExist:
            raise KeyError('Нет такой записи')
