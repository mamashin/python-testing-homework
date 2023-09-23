from typing import Any, final

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView

from server.apps.pictures.container import container
from server.apps.pictures.intrastructure.django.forms import FavouritesForm, DeleteFavouritesForm
from server.apps.pictures.logic.usecases import favourites_list, pictures_fetch
from server.apps.pictures.models import FavouritePicture
from server.common.django.decorators import dispatch_decorator


@final
class IndexView(TemplateView):
    """
    View the :term:`laning`.

    It is a main page open for everyone.
    """

    template_name = 'pictures/pages/index.html'


@final
@dispatch_decorator(login_required)
class DashboardView(CreateView[FavouritePicture, FavouritesForm]):
    """
    View the :term:`dashboard`.

    It is a main page of the whole application.
    This is where we show :term:`pictures` to be saved in :term:`favourites`.
    """

    form_class = FavouritesForm
    template_name = 'pictures/pages/dashboard.html'
    success_url = reverse_lazy('pictures:dashboard')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Innject extra context to template rendering."""
        fetch_puctures = container.instantiate(pictures_fetch.PicturesFetch)

        context = super().get_context_data(**kwargs)
        context['pictures'] = fetch_puctures()  # sync http call, may hang
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add current user to the context."""
        base_kwargs = super().get_form_kwargs()
        base_kwargs['user'] = self.request.user
        return base_kwargs

    def form_valid(self, form: FavouritesForm) -> HttpResponse:
        """Data is valid: show a message about it."""
        messages.success(self.request, 'Добавлено')
        return super().form_valid(form)


@final
@dispatch_decorator(login_required)
class FavouritePicturesView(FormView[FavouritePicture, ]):
    """Show and delete the :term:`favourites`."""

    form_class = DeleteFavouritesForm
    template_name = 'pictures/pages/favourites.html'
    success_url = reverse_lazy('pictures:favourites')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Inject extra context to template rendering."""
        list_favourites = container.instantiate(favourites_list.FavouritesList)

        context = super().get_context_data(**kwargs)
        context['pictures'] = list_favourites(self.request.user.id)  # sync http call, may hang
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add current user to the context."""
        base_kwargs = super().get_form_kwargs()
        base_kwargs['user'] = self.request.user
        return base_kwargs

    def form_valid(self, form: DeleteFavouritesForm) -> HttpResponse:
        """Simple check if data is valid."""
        try:
            form.delete()
            messages.warning(self.request, 'Удалено')
            return super().form_valid(form)
        except KeyError:
            messages.error(self.request, 'Нет такой записи !')
            response = super().form_invalid(form)
            response.status_code = 400
            return response
